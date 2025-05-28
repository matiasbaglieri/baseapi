from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from models.email_verification import EmailVerification
from sqlalchemy import and_
from datetime import datetime, timedelta
from core.logger import logger
import secrets

class EmailService:
    def __init__(self, db: Session):
        self.db = db

    def generate_verification_token(self, user_id: int) -> str:
        """
        Generate a verification token for email verification.
        
        Args:
            user_id (int): ID of the user
            
        Returns:
            str: Verification token
            
        Raises:
            HTTPException: If user not found or other errors occur
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Generate a secure random token
            token = secrets.token_urlsafe(32)
            
            # Create new verification record
            verification = EmailVerification(
                user_id=user_id,
                token=token,
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            
            # Invalidate any existing verification tokens
            existing_tokens = self.db.query(EmailVerification).filter(
                EmailVerification.user_id == user_id
            ).all()
            for existing_token in existing_tokens:
                existing_token.is_used = True
            
            self.db.add(verification)
            self.db.commit()
            
            logger.info(f"Generated verification token for user: {user.email}")
            return token

        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error generating verification token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while generating verification token"
            )

    def verify_email_token(self, token: str) -> User:
        """
        Verify email using the verification token.
        
        Args:
            token (str): Verification token
            
        Returns:
            User: Updated user object
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            # Find valid verification record
            verification = self.db.query(EmailVerification).filter(
                and_(
                    EmailVerification.token == token,
                    EmailVerification.expires_at > datetime.utcnow(),
                    EmailVerification.is_used == False
                )
            ).first()

            if not verification:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired verification token"
                )

            # Get user
            user = self.db.query(User).filter(User.id == verification.user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Update user's verification status
            user.is_verified = True
            verification.is_used = True
            user.updated_at = datetime.utcnow()
            
            self.db.commit()
            logger.info(f"Email verified for user: {user.email}")
            
            return user

        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error verifying email: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while verifying email"
            ) 