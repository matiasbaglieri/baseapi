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

@shared_task
def send_password_change_notification(to_email: str, username: str, ip_address: str = None, user_agent: str = None) -> dict:
    """
    Send a notification email when a user changes their password.
    
    Args:
        to_email (str): Recipient email address
        username (str): Username of the user
        ip_address (str, optional): IP address of the request
        user_agent (str, optional): User agent of the request
        
    Returns:
        dict: Response from Mailgun API
    """
    if not mail_service:
        logger.error("Mail service is not properly configured. Please check your .env-local file.")
        raise ValueError("Mail service is not properly configured")
        
    subject = "Password Changed - Security Alert"
    
    # Format the time
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Create device info string
    device_info = []
    if ip_address:
        device_info.append(f"IP Address: {ip_address}")
    if user_agent:
        device_info.append(f"Browser/Device: {user_agent}")
    device_info_str = "\n".join(device_info) if device_info else "Device information not available"
    
    body = f"""
    Hello {username},
    
    Your password was recently changed at {current_time}.
    
    If you made this change, you can safely ignore this email.
    
    If you did not make this change, please contact support immediately.
    
    Change Details:
    {device_info_str}
    
    For security reasons, all your active sessions have been invalidated.
    You will need to log in again with your new password.
    
    Best regards,
    The BaseAPI Team
    """
    
    return mail_service.send_email(to_email, subject, body)

@shared_task
def send_login_notification(to_email: str, username: str, ip_address: str = None, user_agent: str = None) -> dict:
    """
    Send a notification email when a user logs in.
    
    Args:
        to_email (str): Recipient email address
        username (str): Username of the user
        ip_address (str, optional): IP address of the request
        user_agent (str, optional): User agent of the request
        
    Returns:
        dict: Response from Mailgun API
    """
    if not mail_service:
        logger.error("Mail service is not properly configured. Please check your .env-local file.")
        raise ValueError("Mail service is not properly configured")
        
    subject = "New Login - Security Alert"
    
    # Format the time
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Create device info string
    device_info = []
    if ip_address:
        device_info.append(f"IP Address: {ip_address}")
    if user_agent:
        device_info.append(f"Browser/Device: {user_agent}")
    device_info_str = "\n".join(device_info) if device_info else "Device information not available"
    
    body = f"""
    Hello {username},
    
    A new login was detected for your account at {current_time}.
    
    Login Details:
    {device_info_str}
    
    If this was you, you can safely ignore this email.
    
    If you did not log in, please contact support immediately.
    
    Best regards,
    The BaseAPI Team
    """
    
    return mail_service.send_email(to_email, subject, body) 