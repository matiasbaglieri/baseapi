from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from models.session import Session as SessionModel
from passlib.context import CryptContext
from sqlalchemy import func, and_
from tasks.email_tasks import send_email
from schemas.user import LoginRequest
from .session_service import SessionService
from core.jwt import JWTManager
from core.roles import UserRole
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

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
        Authenticate and login a user.
        
        Args:
            data (LoginRequest): User login credentials
            ip_address (str, optional): IP address of the client
            user_agent (str, optional): User agent string of the client
            
        Returns:
            dict: Login response with user data and JWT tokens
            
        Raises:
            HTTPException: If authentication fails or other errors occur
        """
        try:
            # Find user by email
            user = self.db.query(User).filter(User.email == data.email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            # Verify password using User model's method
            if not user.verify_password(data.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            # Update last login
            user.last_login = func.now()
            
            # Clean up expired sessions for this user
            self.session_service.cleanup_expired_sessions(user.id)
            
        
            # Create new JWT tokens
            tokens = JWTManager.create_tokens_response(
                user_id=user.id,
                email=user.email,
                role=UserRole(user.role)
            )
            
            # Calculate expiration time
            expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            
            # Create new session
            new_session = SessionModel(
                user_id=user.id,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                token_type="bearer",
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=expires_at
            )
            
            self.db.add(new_session)
            access_token = tokens["access_token"]
            refresh_token = tokens["refresh_token"]
        
            self.db.commit()
            
            # Send welcome back email asynchronously
            send_email.delay(
                to_email=user.email,
                subject="Welcome Back!",
                body=f"Welcome back {user.first_name}! You've successfully logged in."
            )
            
            return {
                "message": "Login successful",
                "status": "success",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_verified": user.is_verified,
                    "role": user.role
                },
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                    "expires_in": 900  # 15 minutes in seconds
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 