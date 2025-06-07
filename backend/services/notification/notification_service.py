from sqlalchemy.orm import Session
from models.notification import Notification
from typing import List, Optional, Dict, Any
from datetime import datetime

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_notifications(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[Notification]:
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

        return notifications

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