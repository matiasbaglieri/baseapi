from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    title: str = Field(..., description="Notification title")
    message: str = Field(..., description="Notification message")
    user_id: int = Field(..., description="ID of the user this notification belongs to")
    is_read: bool = Field(False, description="Whether the notification is read")

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Notification title")
    message: Optional[str] = Field(None, description="Notification message")
    is_read: Optional[bool] = Field(None, description="Whether the notification is read")

class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 