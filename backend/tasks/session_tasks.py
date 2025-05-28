from core.celery_app import celery_app
from core.logger import logger
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.session import Session as SessionModel
from datetime import datetime, timedelta
from sqlalchemy import and_
from celery import shared_task

@shared_task(name="cleanup_expired_sessions")
def cleanup_expired_sessions():
    """
    Clean up expired sessions from the database.
    """
    try:
        db = SessionLocal()
        try:
            # Delete expired sessions
            expired_sessions = db.query(SessionModel).filter(
                SessionModel.expires_at < datetime.utcnow()
            ).all()
            
            for session in expired_sessions:
                db.delete(session)
            
            db.commit()
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error cleaning up expired sessions: {str(e)}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error in cleanup_expired_sessions task: {str(e)}")
        raise

@shared_task(name="invalidate_all_sessions")
def invalidate_all_sessions():
    """
    Invalidate all existing sessions.
    This is useful when rotating JWT secret keys or during security incidents.
    """
    try:
        db = SessionLocal()
        try:
            # Mark all sessions as inactive
            db.query(SessionModel).update({
                SessionModel.is_active: False,
                SessionModel.updated_at: datetime.utcnow()
            })
            
            db.commit()
            logger.info("All sessions have been invalidated")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error invalidating sessions: {str(e)}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error in invalidate_all_sessions task: {str(e)}")
        raise

@shared_task(name="invalidate_user_sessions")
def invalidate_user_sessions(user_id: int):
    """
    Invalidate all sessions for a specific user.
    
    Args:
        user_id (int): ID of the user whose sessions should be invalidated
    """
    try:
        db = SessionLocal()
        try:
            # Mark all user's sessions as inactive
            db.query(SessionModel).filter(
                SessionModel.user_id == user_id
            ).update({
                SessionModel.is_active: False,
                SessionModel.updated_at: datetime.utcnow()
            })
            
            db.commit()
            logger.info(f"All sessions for user {user_id} have been invalidated")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error invalidating user sessions: {str(e)}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error in invalidate_user_sessions task: {str(e)}")
        raise

@celery_app.task(name="check_session_activity")
def check_session_activity():
    """
    Check for inactive sessions and invalidate them.
    """
    try:
        db = SessionLocal()
        # Find sessions with no activity for more than 24 hours
        inactive_threshold = datetime.utcnow() - timedelta(hours=24)
        inactive_sessions = db.query(SessionModel).filter(
            and_(
                SessionModel.last_activity < inactive_threshold,
                SessionModel.is_active == True
            )
        ).all()

        for session in inactive_sessions:
            session.is_active = False
            logger.info(f"Invalidated inactive session for user: {session.user_id}")

        db.commit()
        logger.info(f"Checked and invalidated {len(inactive_sessions)} inactive sessions")
        return {"status": "success", "invalidated_sessions": len(inactive_sessions)}

    except Exception as e:
        logger.error(f"Error checking session activity: {str(e)}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close() 