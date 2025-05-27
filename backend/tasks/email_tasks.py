from core.celery_app import celery_app
import time

@celery_app.task(name="send_email")
def send_email(to_email: str, subject: str, body: str):
    """
    Sample task to send an email.
    In a real application, you would integrate with an email service.
    """
    # Simulate email sending
    time.sleep(2)
    print(f"Sending email to {to_email}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    return {"status": "sent", "to": to_email} 