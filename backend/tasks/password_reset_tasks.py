from celery import shared_task
from sqlalchemy.orm import Session
from core.init_db import SessionLocal
from services.user import PasswordResetService
import logging

logger = logging.getLogger(__name__)

@shared_task(name="cleanup_expired_password_resets")
def cleanup_expired_password_resets():
    """
    Celery task to clean up expired password reset tokens.
    This task should be scheduled to run periodically.
    """
    db = SessionLocal()
    try:
        password_reset_service = PasswordResetService(db)
        cleaned_count = password_reset_service.cleanup_expired_tokens() 
        logger.info(f"Cleaned up {cleaned_count} expired password reset tokens")
        return cleaned_count
    except Exception as e:
        logger.error(f"Error cleaning up expired password reset tokens: {str(e)}")
        raise e
    finally:
        db.close() 