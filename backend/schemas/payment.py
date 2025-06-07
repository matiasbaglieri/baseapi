from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class PaymentTransactionCreate(BaseModel):
    amount: float
    currency: str
    stripe_customer_id: str
    description: Optional[str] = None

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    payment_type: str
    payment_method: str
    status: str
    date: datetime
    stripe_payment_intent_id: Optional[str] = None
    data_json: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 