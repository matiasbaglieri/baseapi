from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from models.session import Session as SessionModel
from passlib.context import CryptContext
from sqlalchemy import func, and_
from tasks.email import send_email
from schemas.user import LoginRequest
from .session_service import SessionService
from core.jwt import JWTManager
from core.roles import UserRole
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from core.config import settings
from core.logger import logger
import secrets
from core.security import get_password_hash, verify_password
from tasks.email_tasks import send_password_change_notification
from models.country import Country
from models.city import City

# Load environment variables
load_dotenv()

# Get refresh token expiration days from environment
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginService:
    def __init__(self, db: Session):
        self.db = db
        self.session_service = SessionService(db)

    def login_user(self, data: LoginRequest, ip_address: str = None, user_agent: str = None) -> dict:
        """
        Login a user and return JWT tokens.
        
        Args:
            data (LoginRequest): Login request data
            ip_address (str, optional): IP address of the request
            user_agent (str, optional): User agent of the request
            
        Returns:
            dict: JWT tokens
            
        Raises:
            HTTPException: If login fails
        """
        try:
            # Find user by email
            user = self.db.query(User).filter(User.email == data.email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )

            # Verify password
            if not user.verify_password(data.password):
                # Increment retry count
                user.retry_count += 1
                self.db.commit()
                
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )

            # Check if user is active
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account is deactivated"
                )

            # Check if user is blocked
            if user.is_blocked:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account is blocked"
                )

            # Reset retry count on successful login
            user.retry_count = 0
            user.last_login = datetime.utcnow()
            self.db.commit()

            # Generate JWT tokens
            jwt_manager = JWTManager()
            tokens = jwt_manager.create_tokens_response(
                user_id=user.id,
                email=user.email,
                role=UserRole(user.role)
            )

            # Calculate session expiry
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
            
            # Send login notification email
            try:
                from tasks.email_tasks import send_login_notification
                send_login_notification.delay(
                    to_email=user.email,
                    username=f"{user.first_name} {user.last_name}",
                    ip_address=ip_address,
                    user_agent=user_agent
                )
            except Exception as e:
                logger.error(f"Failed to send login notification email: {str(e)}")
                # Don't raise the exception as the login was successful
            
            logger.info(f"User {user.email} logged in successfully")
            return tokens
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error during login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during login"
            ) 