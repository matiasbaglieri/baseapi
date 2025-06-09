from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from models.session import Session as SessionModel
from sqlalchemy import and_
from datetime import datetime, timedelta
from core.jwt import JWTManager
from core.logger import logger
from schemas.user import UserUpdate, UserResponse
import jwt
from core import settings
import secrets
from core.security import get_password_hash, verify_password
from typing import Optional
from tasks.email_tasks import send_password_change_notification
from models.country import Country
from models.city import City

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

            country_name = None
            country_code = None
            city_name = None
            
            if user.country_id:
                country = self.db.query(Country).filter(Country.id == user.country_id).first()
                if country:
                    country_name = country.name
                    country_code = country.iso2
            
            if user.city_id:
                city = self.db.query(City).filter(City.id == user.city_id).first()
                if city:
                    city_name = city.name
            
            # Create response with country and city names
            response = UserResponse.from_orm(user)
            response.country_name = country_name
            response.country_code = country_code
            response.city_name = city_name
            
            return response

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting current user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching user data"
            )

    def update_user_profile(self, user_id: int, update_data: UserUpdate) -> UserResponse:
        """
        Update user profile information.
        
        Args:
            user_id (int): ID of the user to update
            update_data (UserUpdate): Data to update
            
        Returns:
            UserResponse: Updated user data with country and city names
            
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
            
            # Handle country_id if provided
            if 'country_id' in update_dict:
                country = self.db.query(Country).filter(Country.id == update_dict['country_id']).first()
                if not country:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid country ID"
                    )
                user.country_id = country.id
            # Handle city_id if provided
            if 'city_id' in update_dict:
                city = self.db.query(City).filter(City.id == update_dict['city_id']).first()
                if not city:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid city ID"
                    )
                # Verify city belongs to selected country
                if user.country_id and city.country_id != user.country_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="City does not belong to selected country"
                    )
                user.city_id = city.id

            # Update other fields
            for field, value in update_dict.items():
                if field not in ['country_id', 'city_id']:
                    setattr(user, field, value)

            # Update the updated_at timestamp
            user.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(user)
            
            # Get country and city names
            country_name = None
            country_code = None
            city_name = None
            
            if user.country_id:
                country = self.db.query(Country).filter(Country.id == user.country_id).first()
                if country:
                    country_name = country.name
                    country_code = country.iso2
            
            if user.city_id:
                city = self.db.query(City).filter(City.id == user.city_id).first()
                if city:
                    city_name = city.name
            
            # Create response with country and city names
            response = UserResponse.from_orm(user)
            response.country_name = country_name
            response.country_code = country_code
            response.city_name = city_name
            
            logger.info(f"User profile updated successfully for user: {user.email}")
            return response

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

    def change_password(self, user_id: int, current_password: str, new_password: str, ip_address: str = None, user_agent: str = None) -> dict:
        """
        Change user's password, invalidate all sessions, and create new tokens.
        
        Args:
            user_id (int): ID of the user
            current_password (str): Current password for verification
            new_password (str): New password to set
            ip_address (str, optional): IP address of the request
            user_agent (str, optional): User agent of the request
            
        Returns:
            dict: New access and refresh tokens
            
        Raises:
            HTTPException: If user not found or current password is incorrect
        """
        try:
            # Get user and verify current password
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            if not user.verify_password(current_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Current password is incorrect"
                )
            
            # Update password
            user.set_password(new_password)
            user.updated_at = datetime.utcnow()
            
            # Delete all existing sessions
            self.db.query(SessionModel).filter(SessionModel.user_id == user_id).delete()
            
            # Create new tokens
            tokens = JWTManager.create_tokens_response(
                user_id=user.id,
                email=user.email,
                role=user.role
            )
            
            # Calculate session expiration time
            expires_at = datetime.utcnow() + timedelta(days=settings.SESSION_EXPIRY_DAYS)
            
            # Create new session
            new_session = SessionModel(
                user_id=user.id,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                token_type="bearer",
                ip_address=ip_address,
                user_agent=user_agent,
                created_at=datetime.utcnow(),
                expires_at=expires_at,
                last_activity=datetime.utcnow(),
                is_active=True
            )
            self.db.add(new_session)
            
            # Commit all changes
            self.db.commit()
            
            # Send password change notification email
            try:
                send_password_change_notification.delay(
                    to_email=user.email,
                    username=f"{user.first_name} {user.last_name}",
                    ip_address=ip_address,
                    user_agent=user_agent
                )
            except Exception as e:
                logger.error(f"Failed to send password change notification email: {str(e)}")
                # Don't raise the exception as the password change was successful
            
            logger.info(f"Password changed successfully for user {user.email}")
            return tokens
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error changing password: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while changing password"
            ) 