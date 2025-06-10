from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class SubscriptionBase(BaseModel):
    name: str
    subscription_type: str
    currency: str
    price: float
    features: Optional[Dict[str, Any]] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    name: Optional[str] = None
    subscription_type: Optional[str] = None
    currency: Optional[str] = None
    price: Optional[float] = None
    features: Optional[Dict[str, Any]] = None

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
    payment_method_id: Optional[str] = None
    data_json: Optional[Dict[str, Any]] = None

class SubscriptionUserResponse(BaseModel):
    id: int
    user_id: int
    subscription_id: int
    status: str
    data_json: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    stripe_subscription_id: Optional[str] = None
    client_secret: Optional[str] = None

    class Config:
        from_attributes = True