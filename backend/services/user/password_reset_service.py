from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from models.password_reset import PasswordReset
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import secrets
from tasks.password_reset_tasks import send_password_reset_notification
from core.config import settings
from passlib.context import CryptContext
from core.logger import logger

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
                    PasswordReset.is_used == False
                )
            ).all()
            
            # Mark tokens as used
            for token in expired_tokens:
                token.is_used = True
            
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
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Invalidate any existing reset tokens
            existing_tokens = self.db.query(PasswordReset).filter(
                PasswordReset.user_id == user.id
            ).all()
            for token in existing_tokens:
                token.is_used = True

            # Generate a secure token
            token = secrets.token_urlsafe(32)

            # Create new reset token
            reset_token = PasswordReset(
                user_id=user.id,
                token=token,
                expires_at=datetime.utcnow() + timedelta(hours=24),
                is_used=False
            )
            self.db.add(reset_token)
            self.db.commit()

            # Send password reset email using the dedicated task
            send_password_reset_notification.delay(user.id, reset_token.token)
            logger.info(f"Password reset email sent to user: {user.email}")

            return {
                "message": "Password reset email sent",
                "status": "success"
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating password reset: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing your request"
            )

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
                and_(
                    PasswordReset.token == token,
                    PasswordReset.is_used == False,
                    PasswordReset.expires_at > datetime.utcnow()
                )
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
            # Find valid reset token
            reset_token = self.db.query(PasswordReset).filter(
                and_(
                    PasswordReset.token == token,
                    PasswordReset.expires_at > datetime.utcnow(),
                    PasswordReset.is_used == False
                )
            ).first()

            if not reset_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired token"
                )

            # Get user and update password
            user = self.db.query(User).filter(User.id == reset_token.user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Update password
            user.set_password(new_password)
            reset_token.is_used = True
            self.db.commit()

            # Send confirmation email using the dedicated task
            send_password_reset_notification.delay(
                user.id,
                "Password Reset Successful"
            )
            logger.info(f"Password reset successful for user: {user.email}")

            return {
                "message": "Password reset successful",
                "status": "success"
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error resetting password: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing your request"
            ) 