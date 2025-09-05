import httpx
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class BkashService:
    def __init__(self):
        self.base_url = os.getenv("BKASH_BASE_URL")
        self.app_key = os.getenv("BKASH_APP_KEY")
        self.app_secret = os.getenv("BKASH_APP_SECRET")
        self.username = os.getenv("BKASH_USERNAME")
        self.password = os.getenv("BKASH_PASSWORD")
        self.token = None
        self.token_expires = None

    async def get_token(self):
        """Get access token from bKash"""
        if self.token and self.token_expires and datetime.now() < self.token_expires:
            return self.token

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "username": self.username,
            "password": self.password
        }

        data = {
            "app_key": self.app_key,
            "app_secret": self.app_secret
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tokenized/checkout/token/grant",
                json=data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                self.token = result.get("id_token")
                self.token_expires = datetime.now().timestamp() + 3000
                return self.token
            else:
                raise Exception(f"Failed to get token: {response.text}")

    async def create_payment(self, amount: float, invoice_number: str, intent: str = "sale"):
        """Create payment with bKash"""
        token = await self.get_token()
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "authorization": token,
            "x-app-key": self.app_key
        }

        data = {
            "mode": "0011",
            "payerReference": invoice_number,
            "callbackURL": "http://localhost:8000/payment/callback",
            "amount": str(amount),
            "currency": "BDT",
            "intent": intent,
            "merchantInvoiceNumber": invoice_number
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tokenized/checkout/create",
                json=data,
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to create payment: {response.text}")

    async def execute_payment(self, payment_id: str):
        """Execute payment with bKash"""
        token = await self.get_token()
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "authorization": token,
            "x-app-key": self.app_key
        }

        data = {
            "paymentID": payment_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tokenized/checkout/execute",
                json=data,
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to execute payment: {response.text}")

    async def query_payment(self, payment_id: str):
        """Query payment status from bKash"""
        token = await self.get_token()
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "authorization": token,
            "x-app-key": self.app_key
        }

        data = {
            "paymentID": payment_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tokenized/checkout/payment/status",
                json=data,
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to query payment: {response.text}")