from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SubscriptionBase(BaseModel):
    name: str
    subscription_type: str
    currency: str
    amount: float

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionResponse(SubscriptionBase):
    id: int
    stripe_product_id: Optional[str] = None
    stripe_price_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SubscriptionCreateResponse(BaseModel):
    subscription_id: str
    client_secret: str

class SubscriptionUserCreate(BaseModel):
    subscription_id: int
    payment_method: str
    amount: float
    currency: str = "USD"
    
    class Config:
        from_attributes = True