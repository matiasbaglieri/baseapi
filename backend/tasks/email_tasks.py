from celery import shared_task
from core.mail import mail_service
from core.logger import logger
from core.config import settings
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from datetime import datetime, timedelta
from sqlalchemy import and_

@shared_task
def send_email(to_email: str, subject: str, body: str) -> dict:
    """
    Send an email using Mailgun API.
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        body (str): Email body
        
    Returns:
        dict: Response from Mailgun API
    """
    if not mail_service:
        logger.error("Mail service is not properly configured. Please check your .env-local file.")
        raise ValueError("Mail service is not properly configured")
        
    return mail_service.send_email(to_email, subject, body)

@shared_task
def send_welcome_email(to_email: str, username: str) -> dict:
    """
    Send a welcome email to a new user.
    
    Args:
        to_email (str): Recipient email address
        username (str): Username of the new user
        
    Returns:
        dict: Response from Mailgun API
    """
    if not mail_service:
        logger.error("Mail service is not properly configured. Please check your .env-local file.")
        raise ValueError("Mail service is not properly configured")
        
    subject = "Welcome to BaseAPI!"
    body = f"""
    Hello {username},
    
    Welcome to BaseAPI! We're excited to have you on board.
    
    Best regards,
    The BaseAPI Team
    """
    return mail_service.send_email(to_email, subject, body)

@shared_task
def send_password_reset_email(to_email: str, reset_token: str) -> dict:
    """
    Send a password reset email.
    
    Args:
        to_email (str): Recipient email address
        reset_token (str): Password reset token
        
    Returns:
        dict: Response from Mailgun API
    """
    if not mail_service:
        logger.error("Mail service is not properly configured. Please check your .env-local file.")
        raise ValueError("Mail service is not properly configured")
        
    subject = "Password Reset Request"
    body = f"""
    Hello,
    
    You have requested to reset your password. Please use the following token:
    
    {reset_token}
    
    This token will expire in 24 hours.
    
    If you did not request this password reset, please ignore this email.
    
    Best regards,
    The BaseAPI Team
    """
    return mail_service.send_email(to_email, subject, body) 