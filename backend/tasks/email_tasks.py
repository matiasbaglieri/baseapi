from core.celery_app import celery_app
from core.logger import logger
from core.config import settings
from core.mail import MailService
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from datetime import datetime, timedelta
from sqlalchemy import and_

@celery_app.task(name="send_email")
def send_email(to_email: str, subject: str, body: str):
    """
    Send an email using the mail service.
    """
    try:
        mail_service = MailService()
        mail_service.send_email(to_email, subject, body)
        logger.info(f"Email sent to {to_email}")
        return {"status": "success", "to_email": to_email}
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return {"status": "error", "error": str(e)}

@celery_app.task(name="send_welcome_email")
def send_welcome_email(to_email: str, first_name: str):
    """
    Send welcome email to newly registered users.
    """
    subject = "Welcome to Our Platform!"
    body = f"""
    Hello {first_name},

    Welcome to our platform! We're excited to have you on board.

    Best regards,
    The Team
    """
    html_body = f"""
    <h1>Welcome to Our Platform!</h1>
    <p>Hello {first_name},</p>
    <p>Welcome to our platform! We're excited to have you on board.</p>
    <p>Best regards,<br>The Team</p>
    """
    return send_email.delay(to_email, subject, body, html_body)

@celery_app.task(name="send_password_reset_email")
def send_password_reset_email(to_email: str, reset_token: str):
    """
    Send password reset email.
    """
    try:
        mail_service = MailService()
        subject = "Password Reset Request"
        body = f"""
        Hello,
        
        You have requested to reset your password. Please use the following token to reset your password:
        
        {reset_token}
        
        This token will expire in 24 hours.
        
        If you did not request this password reset, please ignore this email.
        
        Best regards,
        Your App Team
        """
        mail_service.send_email(to_email, subject, body)
        logger.info(f"Password reset email sent to {to_email}")
        return {"status": "success", "to_email": to_email}
    except Exception as e:
        logger.error(f"Error sending password reset email: {str(e)}")
        return {"status": "error", "error": str(e)}

@celery_app.task(name="send_verification_email")
def send_verification_email(to_email: str, verification_token: str):
    """
    Send email verification email.
    """
    try:
        mail_service = MailService()
        subject = "Verify Your Email"
        body = f"""
        Hello,
        
        Thank you for registering. Please use the following token to verify your email:
        
        {verification_token}
        
        This token will expire in 24 hours.
        
        Best regards,
        Your App Team
        """
        mail_service.send_email(to_email, subject, body)
        logger.info(f"Verification email sent to {to_email}")
        return {"status": "success", "to_email": to_email}
    except Exception as e:
        logger.error(f"Error sending verification email: {str(e)}")
        return {"status": "error", "error": str(e)} 