from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class NotificationBase(BaseModel):
    title: str
    action: str
    data_json: Optional[Dict[str, Any]] = None
    
class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 