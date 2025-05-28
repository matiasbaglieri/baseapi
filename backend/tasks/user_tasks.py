from core.celery_app import celery_app
from core.logger import logger
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from datetime import datetime, timedelta
from sqlalchemy import and_

@celery_app.task(name="cleanup_inactive_users")
def cleanup_inactive_users():
    """
    Clean up inactive users who haven't logged in for a long time.
    """
    try:
        db = SessionLocal()
        # Find users who haven't logged in for 6 months
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        inactive_users = db.query(User).filter(
            and_(
                User.last_login < six_months_ago,
                User.is_active == True
            )
        ).all()

        for user in inactive_users:
            user.is_active = False
            logger.info(f"Deactivated inactive user: {user.email}")

        db.commit()
        logger.info(f"Cleaned up {len(inactive_users)} inactive users")
        return {"status": "success", "deactivated_users": len(inactive_users)}

    except Exception as e:
        logger.error(f"Error cleaning up inactive users: {str(e)}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close()

@celery_app.task(name="send_inactivity_notification")
def send_inactivity_notification(user_id: int):
    """
    Send notification to users who haven't logged in for a while.
    """
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            logger.error(f"User not found: {user_id}")
            return {"status": "error", "error": "User not found"}

        # Send email notification
        from tasks.email_tasks import send_email
        subject = "We Miss You!"
        body = f"""
        Hello {user.first_name},

        We noticed you haven't logged in for a while. We hope everything is okay!
        Come back and check out what's new.

        Best regards,
        The Team
        """
        html_body = f"""
        <h1>We Miss You!</h1>
        <p>Hello {user.first_name},</p>
        <p>We noticed you haven't logged in for a while. We hope everything is okay!</p>
        <p>Come back and check out what's new.</p>
        <p>Best regards,<br>The Team</p>
        """
        
        send_email.delay(user.email, subject, body, html_body)
        logger.info(f"Sent inactivity notification to user: {user.email}")
        return {"status": "success", "user_id": user_id}

    except Exception as e:
        logger.error(f"Error sending inactivity notification: {str(e)}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close() 