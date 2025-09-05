from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: str
    name: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    subscription_id: int
    amount: float

class PaymentExecute(BaseModel):
    payment_id: str

class PaymentResponse(BaseModel):
    id: int
    amount: float
    status: str
    bkash_payment_id: Optional[str]
    transaction_id: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True