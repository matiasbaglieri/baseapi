from sqlalchemy.orm import Session
from models.session import Session as SessionModel
from sqlalchemy import and_
from datetime import datetime

class SessionService:
    def __init__(self, db: Session):
        self.db = db

    def cleanup_expired_sessions(self, user_id: int = None) -> int:
        """
        Clean up expired sessions for a specific user or all users.
        
        Args:
            user_id (int, optional): If provided, only clean up sessions for this user
            
        Returns:
            int: Number of sessions cleaned up
        """
        try:
            # Build query conditions
            conditions = [
                SessionModel.expires_at <= datetime.utcnow(),
                SessionModel.is_active == True
            ]
            
            # Add user_id condition if provided
            if user_id:
                conditions.append(SessionModel.user_id == user_id)
            
            # Find and deactivate expired sessions
            expired_sessions = self.db.query(SessionModel).filter(
                and_(*conditions)
            ).all()
            
            # Deactivate sessions
            for session in expired_sessions:
                session.is_active = False
            
            self.db.commit()
            return len(expired_sessions)
            
        except Exception as e:
            self.db.rollback()
            raise e 