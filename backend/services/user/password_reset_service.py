from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User
from models.password_reset import PasswordReset
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import secrets
from tasks.email_tasks import send_email
from core.config import settings
from passlib.context import CryptContext
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordResetService:
    def __init__(self, db: Session):
        self.db = db

    def cleanup_expired_tokens(self) -> int:
        """
        Clean up expired password reset tokens.
        
        Returns:
            int: Number of tokens cleaned up
        """
        try:
            # Find expired tokens that are still marked as valid
            expired_tokens = self.db.query(PasswordReset).filter(
                and_(
                    PasswordReset.expires_at <= datetime.utcnow(),
                    PasswordReset.is_valid == True
                )
            ).all()
            
            # Mark tokens as invalid
            for token in expired_tokens:
                token.is_valid = False
            
            self.db.commit()
            return len(expired_tokens)
            
        except Exception as e:
            self.db.rollback()
            raise e

    def create_password_reset(self, email: str) -> dict:
        """
        Create a password reset token for a user.
        
        Args:
            email (str): User's email address
            
        Returns:
            dict: Response with status message
            
        Raises:
            HTTPException: If user not found or other errors occur
        """
        try:
            # Find user by email
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                # Return success even if user not found to prevent email enumeration
                return {
                    "message": "If your email is registered, you will receive a password reset link.",
                    "status": "success"
                }
            
            # Create password reset token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=24)  # 24 hour expiry
            
            # Create password reset record
            password_reset = PasswordReset(
                user_id=user.id,
                token=token,
                expires_at=expires_at,
                is_valid=True
            )
            
            self.db.add(password_reset)
            self.db.commit()
            
            # Generate reset link
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            logger.info(f"Generated password reset link for user {user.email}: {reset_link}")
            
            # Send password reset email
            send_email.delay(
                to_email=user.email,
                subject="Password Reset Request",
                body=f"""
                Hello {user.first_name},
                
                You have requested to reset your password. Click the link below to reset your password:
                {reset_link}
                
                This link will expire in 24 hours.
                
                If you did not request this password reset, please ignore this email.
                
                Best regards,
                Your App Team
                """
            )
            
            return {
                "message": "If your email is registered, you will receive a password reset link.",
                "status": "success"
            }
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def verify_reset_token(self, token: str) -> User:
        """
        Verify a password reset token.
        
        Args:
            token (str): Password reset token
            
        Returns:
            User: User associated with the token
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            # Find valid password reset record
            reset_record = self.db.query(PasswordReset).filter(
                PasswordReset.token == token,
                PasswordReset.is_valid == True,
                PasswordReset.expires_at > datetime.utcnow()
            ).first()
            
            if not reset_record:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid or expired password reset token"
                )
            
            return reset_record.user
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def reset_password(self, token: str, new_password: str) -> dict:
        """
        Reset a user's password using a valid token.
        
        Args:
            token (str): Password reset token
            new_password (str): New password
            
        Returns:
            dict: Response with status message
            
        Raises:
            HTTPException: If token is invalid or other errors occur
        """
        try:
            # Verify token and get user
            user = self.verify_reset_token(token)
            
            # Update password
            user.password = pwd_context.hash(new_password)
            
            # Mark reset token as used
            reset_record = self.db.query(PasswordReset).filter(
                and_(
                    PasswordReset.token == token,
                    PasswordReset.expires_at > datetime.utcnow(),
                    PasswordReset.is_valid == True
                )
            ).first()
            
            if not reset_record:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid or expired password reset token"
                )
            
            reset_record.is_valid = False
            reset_record.used_at = datetime.utcnow()
            
            self.db.commit()
            
            # Send confirmation email
            send_email.delay(
                to_email=user.email,
                subject="Password Reset Successful",
                body=f"""
                Hello {user.first_name},
                
                Your password has been successfully reset.
                
                If you did not make this change, please contact support immediately.
                
                Best regards,
                Your App Team
                """
            )
            
            return {
                "message": "Password has been reset successfully",
                "status": "success"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e)) 