from core.celery_app import celery_app
from core.logger import logger
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.session import Session as SessionModel
from datetime import datetime, timedelta
from sqlalchemy import and_

@celery_app.task(name="cleanup_expired_sessions")
def cleanup_expired_sessions():
    """
    Clean up expired sessions from the database.
    """
    try:
        db = SessionLocal()
        # Find and delete expired sessions
        expired_sessions = db.query(SessionModel).filter(
            SessionModel.expires_at < datetime.utcnow()
        ).all()

        for session in expired_sessions:
            db.delete(session)
            logger.info(f"Deleted expired session for user: {session.user_id}")

        db.commit()
        logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        return {"status": "success", "deleted_sessions": len(expired_sessions)}

    except Exception as e:
        logger.error(f"Error cleaning up expired sessions: {str(e)}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close()

@celery_app.task(name="invalidate_user_sessions")
def invalidate_user_sessions(user_id: int):
    """
    Invalidate all sessions for a specific user.
    """
    try:
        db = SessionLocal()
        # Find and invalidate all sessions for the user
        sessions = db.query(SessionModel).filter(
            SessionModel.user_id == user_id
        ).all()

        for session in sessions:
            session.is_active = False
            logger.info(f"Invalidated session for user: {user_id}")

        db.commit()
        logger.info(f"Invalidated {len(sessions)} sessions for user: {user_id}")
        return {"status": "success", "invalidated_sessions": len(sessions)}

    except Exception as e:
        logger.error(f"Error invalidating user sessions: {str(e)}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close()

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