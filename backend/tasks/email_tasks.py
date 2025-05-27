from core.celery_app import celery_app
from core.logger import logger
from core.mail import mail_service

@celery_app.task(name="send_email")
def send_email(to_email: str, subject: str, body: str, html_body: str = None):
    """
    Send an email using Mailgun service.
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        body (str): Plain text email body
        html_body (str, optional): HTML email body
    """
    try:
        response = mail_service.send_email(
            to_email=to_email,
            subject=subject,
            body=body,
            html_body=html_body
        )
        return {"status": "sent", "to": to_email, "response": response}
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return {"status": "failed", "to": to_email, "error": str(e)} 