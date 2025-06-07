from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class SubscriptionUserBase(BaseModel):
    subscription_id: int
    stripe_customer_id: str

class SubscriptionUserCreate(SubscriptionUserBase):
    pass

class SubscriptionUserResponse(SubscriptionUserBase):
    id: int
    user_id: int
    status: str
    start_date: datetime
    end_date: Optional[datetime] = None
    data_json: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 