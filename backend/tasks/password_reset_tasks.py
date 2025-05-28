from core.celery_app import celery_app
from core.logger import logger
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.password_reset import PasswordReset
from models.user import User
from datetime import datetime, timedelta
from sqlalchemy import and_
from tasks.email_tasks import send_password_reset_email

@celery_app.task(name="cleanup_expired_password_resets")
def cleanup_expired_password_resets():
    """
    Clean up expired password reset tokens.
    """
    try:
        db = SessionLocal()
        # Find and delete expired password reset tokens
        expired_resets = db.query(PasswordReset).filter(
            PasswordReset.expires_at < datetime.utcnow()
        ).all()

        for reset in expired_resets:
            db.delete(reset)
            logger.info(f"Deleted expired password reset token for user: {reset.user_id}")

        db.commit()
        logger.info(f"Cleaned up {len(expired_resets)} expired password reset tokens")
        return {"status": "success", "deleted_tokens": len(expired_resets)}

    except Exception as e:
        logger.error(f"Error cleaning up expired password reset tokens: {str(e)}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close()

@celery_app.task(name="send_password_reset_notification")
def send_password_reset_notification(user_id: int, reset_token: str):
    """
    Send password reset notification email.
    """
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            logger.error(f"User not found: {user_id}")
            return {"status": "error", "error": "User not found"}

        # Send password reset email
        send_password_reset_email.delay(user.email, reset_token)
        logger.info(f"Sent password reset notification to user: {user.email}")
        return {"status": "success", "user_id": user_id}

    except Exception as e:
        logger.error(f"Error sending password reset notification: {str(e)}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close()

@celery_app.task(name="invalidate_user_password_resets")
def invalidate_user_password_resets(user_id: int):
    """
    Invalidate all password reset tokens for a specific user.
    """
    try:
        db = SessionLocal()
        # Find and invalidate all password reset tokens for the user
        resets = db.query(PasswordReset).filter(
            PasswordReset.user_id == user_id
        ).all()

        for reset in resets:
            reset.is_used = True
            logger.info(f"Invalidated password reset token for user: {user_id}")

        db.commit()
        logger.info(f"Invalidated {len(resets)} password reset tokens for user: {user_id}")
        return {"status": "success", "invalidated_tokens": len(resets)}

    except Exception as e:
        logger.error(f"Error invalidating password reset tokens: {str(e)}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close() 