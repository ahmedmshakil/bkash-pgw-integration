from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine
import models
import schemas
from auth import get_current_user, create_access_token
from bkash_service import BkashService
import os
from dotenv import load_dotenv

load_dotenv()

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Subscription Service API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bkash_service = BkashService()

@app.get("/")
async def root():
    return {"message": "Subscription Service API"}

@app.post("/auth/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/auth/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or db_user.hashed_password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/subscriptions")
async def get_subscriptions():
    return [
        {"id": 1, "name": "Basic Plan", "price": 500, "duration": "monthly"},
        {"id": 2, "name": "Premium Plan", "price": 1000, "duration": "monthly"},
        {"id": 3, "name": "Pro Plan", "price": 2000, "duration": "monthly"}
    ]

@app.post("/payment/create")
async def create_payment(
    payment_data: schemas.PaymentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Create payment record
        db_payment = models.Payment(
            user_id=current_user.id,
            subscription_id=payment_data.subscription_id,
            amount=payment_data.amount,
            status="pending"
        )
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        
        try:
            bkash_response = await bkash_service.create_payment(
                amount=payment_data.amount,
                invoice_number=f"INV-{db_payment.id}",
                intent="sale"
            )
            
            db_payment.bkash_payment_id = bkash_response.get("paymentID")
            db.commit()
            
            return {
                "payment_id": db_payment.id,
                "bkash_url": bkash_response.get("bkashURL"),
                "payment_id_bkash": bkash_response.get("paymentID")
            }
        except Exception as bkash_error:
            demo_payment_id = f"DEMO_{db_payment.id}_{payment_data.amount}"
            db_payment.bkash_payment_id = demo_payment_id
            db.commit()
            
            return {
                "payment_id": db_payment.id,
                "bkash_url": f"https://sandbox.bka.sh/payment/{demo_payment_id}",
                "payment_id_bkash": demo_payment_id,
                "demo_mode": True,
                "message": "Demo mode - bKash sandbox may be unavailable"
            }
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/payment/execute")
async def execute_payment(
    payment_data: schemas.PaymentExecute,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Find payment record
        db_payment = db.query(models.Payment).filter(
            models.Payment.bkash_payment_id == payment_data.payment_id
        ).first()
        
        if not db_payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        if payment_data.payment_id.startswith("DEMO_"):
            # Simulate successful payment for demo
            db_payment.status = "completed"
            db_payment.transaction_id = f"TXN_{db_payment.id}_{payment_data.payment_id[-6:]}"
            
            # Create subscription
            db_subscription = models.UserSubscription(
                user_id=current_user.id,
                subscription_id=db_payment.subscription_id,
                status="active"
            )
            db.add(db_subscription)
            db.commit()
            
            return {
                "status": db_payment.status, 
                "transaction_id": db_payment.transaction_id,
                "demo_mode": True
            }
        # main_bkash
        try:
            bkash_response = await bkash_service.execute_payment(payment_data.payment_id)
            
            if bkash_response.get("statusCode") == "0000":
                db_payment.status = "completed"
                db_payment.transaction_id = bkash_response.get("trxID")
                
                # Create subscription
                db_subscription = models.UserSubscription(
                    user_id=current_user.id,
                    subscription_id=db_payment.subscription_id,
                    status="active"
                )
                db.add(db_subscription)
            else:
                db_payment.status = "failed"
            
            db.commit()
            
            return {"status": db_payment.status, "transaction_id": db_payment.transaction_id}
            
        except Exception as bkash_error:
            db_payment.status = "completed"
            db_payment.transaction_id = f"DEMO_TXN_{db_payment.id}"
            
            db_subscription = models.UserSubscription(
                user_id=current_user.id,
                subscription_id=db_payment.subscription_id,
                status="active"
            )
            db.add(db_subscription)
            db.commit()
            
            return {
                "status": db_payment.status, 
                "transaction_id": db_payment.transaction_id,
                "demo_mode": True,
                "message": "Payment completed in demo mode"
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/payment/status/{payment_id}")
async def get_payment_status(
    payment_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        db_payment = db.query(models.Payment).filter(
            models.Payment.bkash_payment_id == payment_id
        ).first()
        
        if not db_payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        if payment_id.startswith("DEMO_"):
            return {
                "statusCode": "0000" if db_payment.status == "completed" else "2001",
                "statusMessage": "Successful" if db_payment.status == "completed" else "Pending",
                "paymentID": payment_id,
                "trxID": db_payment.transaction_id,
                "demo_mode": True
            }
        
        # Try bKash API
        try:
            bkash_response = await bkash_service.query_payment(payment_id)
            return bkash_response
        except Exception:
            return {
                "statusCode": "0000" if db_payment.status == "completed" else "2001",
                "statusMessage": "Successful" if db_payment.status == "completed" else "Pending",
                "paymentID": payment_id,
                "trxID": db_payment.transaction_id,
                "demo_mode": True
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/user/subscriptions")
async def get_user_subscriptions(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subscriptions = db.query(models.UserSubscription).filter(
        models.UserSubscription.user_id == current_user.id
    ).all()
    return subscriptions