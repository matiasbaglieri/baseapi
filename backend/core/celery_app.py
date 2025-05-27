from celery import Celery
from .config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Celery Configuration
CELERY_BROKER_URL = settings.CELERY_BROKER_URL
CELERY_RESULT_BACKEND = settings.CELERY_RESULT_BACKEND

# Initialize Celery
celery_app = Celery(
    "baseapi",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        'tasks.email_tasks',
        'tasks.user_tasks',
        'tasks.session_tasks',
        'tasks.password_reset_tasks'
    ]
)

def init_celery():
    """Initialize Celery with application settings."""
    try:
        celery_app.conf.update(
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json',
            timezone='UTC',
            enable_utc=True
        )
        logger.info("Celery initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Celery: {str(e)}")
        raise

def shutdown_celery():
    """Cleanup Celery resources."""
    try:
        celery_app.control.shutdown()
        logger.info("Celery shutdown successfully")
    except Exception as e:
        logger.error(f"Error shutting down Celery: {str(e)}")
        raise 