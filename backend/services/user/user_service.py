from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from models.session import Session as SessionModel
from sqlalchemy import and_
from datetime import datetime, timedelta
from core.jwt import JWTManager
from core.logger import logger
from schemas.user import UserUpdate
import jwt
from core import settings
import secrets

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_current_user(self, access_token: str) -> User:
        """
        Get current user data from access token.
        
        Args:
            access_token (str): JWT access token
            
        Returns:
            User: User object
            
        Raises:
            HTTPException: If token is invalid or user not found
        """
        try:
            # Verify the access token
            payload = JWTManager.verify_token(access_token)
            user_id = int(payload["sub"])

            # Find active session
            session = self.db.query(SessionModel).filter(
                and_(
                    SessionModel.user_id == user_id,
                    SessionModel.access_token == access_token,
                    SessionModel.expires_at > datetime.utcnow(),
                    SessionModel.is_active == True
                )
            ).first()

            if not session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired session"
                )

            # Get user data
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Update last activity
            session.last_activity = datetime.utcnow()
            self.db.commit()

            return user

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting current user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching user data"
            )

    def update_user_profile(self, user_id: int, update_data: UserUpdate) -> User:
        """
        Update user profile information.
        
        Args:
            user_id (int): ID of the user to update
            update_data (UserUpdate): Data to update
            
        Returns:
            User: Updated user object
            
        Raises:
            HTTPException: If user not found or other errors occur
        """
        try:
            # Get user from database
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Update only the fields that are provided
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(user, field, value)

            # Update the updated_at timestamp
            user.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"User profile updated successfully for user: {user.email}")
            return user

        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing your request"
            )

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
            
            # Store the token in the user's verification_token field
            user.verification_token = token
            user.verification_token_expires = datetime.utcnow() + timedelta(hours=24)
            
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
            # Find user with matching token
            user = self.db.query(User).filter(
                and_(
                    User.verification_token == token,
                    User.verification_token_expires > datetime.utcnow()
                )
            ).first()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired verification token"
                )

            # Update user's verification status
            user.is_verified = True
            user.verification_token = None
            user.verification_token_expires = None
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