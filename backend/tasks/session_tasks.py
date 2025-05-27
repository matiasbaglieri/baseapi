from celery import shared_task
from sqlalchemy.orm import Session
from models.session import Session as SessionModel
from sqlalchemy import and_
from datetime import datetime
from core.init_db import SessionLocal
import logging

logger = logging.getLogger(__name__)

@shared_task(name="cleanup_expired_sessions")
def cleanup_expired_sessions():
    """
    Celery task to clean up expired sessions.
    This task should be scheduled to run periodically.
    """
    db = SessionLocal()
    try:
        # Build query conditions
        conditions = [
            SessionModel.expires_at <= datetime.utcnow(),
            SessionModel.is_active == True
        ]
        
        # Find and deactivate expired sessions
        expired_sessions = db.query(SessionModel).filter(
            and_(*conditions)
        ).all()
        
        # Deactivate sessions
        for session in expired_sessions:
            session.is_active = False
        
        db.commit()
        cleaned_count = len(expired_sessions)
        logger.info(f"Cleaned up {cleaned_count} expired sessions")
        return cleaned_count
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error cleaning up expired sessions: {str(e)}")
        raise e
    finally:
        db.close() 