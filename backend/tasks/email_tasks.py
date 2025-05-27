from core.celery_app import celery_app
from core.logger import logger
import time

@celery_app.task(name="send_email")
def send_email(to_email: str, subject: str, body: str):
    """
    Sample task to send an email.
    In a real application, you would integrate with an email service.
    """
    # Simulate email sending
    time.sleep(2)
    logger.info(f"Sending email to {to_email}")
    logger.info(f"Subject: {subject}")
    logger.info(f"Body: {body}")
    return {"status": "sent", "to": to_email} 