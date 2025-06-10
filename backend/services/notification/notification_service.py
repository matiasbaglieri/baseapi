from sqlalchemy.orm import Session
from models.notification import Notification
from typing import List, Optional, Dict, Any
from datetime import datetime

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def _convert_notification_to_dict(self, notification: Notification) -> Dict[str, Any]:
        """Convert notification to dictionary with required fields"""
        return {
            "id": notification.id,
            "user_id": notification.user_id,
            "title": notification.title,
            "message": notification.data_json.get("message", notification.title),  # Use title as fallback
            "is_read": notification.is_read,
            "action": notification.action,
            "data_json": notification.data_json,
            "created_at": notification.created_at,
            "updated_at": notification.updated_at
        }

    def get_user_notifications(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get paginated list of user's notifications and mark unread ones as read
        """
        # First get paginated notifications
        notifications = self.db.query(Notification).filter(
            Notification.user_id == user_id
        ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

        # Get IDs of unread notifications in the current page
        unread_ids = [n.id for n in notifications if not n.is_read]

        # Mark unread notifications as read
        if unread_ids:
            self.db.query(Notification).filter(
                Notification.id.in_(unread_ids)
            ).update(
                {Notification.is_read: True, Notification.updated_at: datetime.utcnow()},
                synchronize_session=False
            )
            self.db.commit()

        # Convert notifications to dictionaries with required fields
        return [self._convert_notification_to_dict(n) for n in notifications]

    def create_notification(
        self,
        user_id: int,
        title: str,
        action: str,
        data_json: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """
        Create a new notification
        """
        notification = Notification(
            user_id=user_id,
            title=title,
            action=action,
            data_json=data_json,
            is_read=False
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return notification