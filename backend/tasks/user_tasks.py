from core.celery_app import celery_app
from models.user import User
from sqlalchemy.orm import Session
from core.init_db import SessionLocal

@celery_app.task(name="cleanup_inactive_users")
def cleanup_inactive_users():
    """
    Sample task to clean up inactive users.
    """
    db = SessionLocal()
    try:
        # Example: Delete users who haven't logged in for 30 days
        # In a real application, you would implement proper cleanup logic
        print("Cleaning up inactive users...")
        return {"status": "completed", "message": "Cleanup task finished"}
    finally:
        db.close() 