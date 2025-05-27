from celery import Celery
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Celery Configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Initialize Celery
celery_app = Celery(
    "baseapi",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

def init_celery():
    """Initialize Celery configuration."""
    logger.info("Initializing Celery...")
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
    )
    logger.info("Celery initialized successfully")

def shutdown_celery():
    """Shutdown Celery gracefully."""
    logger.info("Shutting down Celery...")
    try:
        # Close Celery connection pool
        celery_app.control.broadcast('shutdown')
        logger.info("Celery shutdown signal sent")
        
        # Close Celery connection
        if celery_app.connection():
            celery_app.connection().close()
            logger.info("Celery connection closed")
    except Exception as e:
        logger.error(f"Error during Celery shutdown: {str(e)}")
    logger.info("Celery shutdown complete") 