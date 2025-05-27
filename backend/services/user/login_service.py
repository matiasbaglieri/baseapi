from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User
from models.session import Session as SessionModel
from passlib.context import CryptContext
from sqlalchemy import func, and_
from tasks.email_tasks import send_email
from schemas.user import LoginRequest
from .session_service import SessionService
import secrets
from datetime import datetime, timedelta

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
            dict: Login response with user data and session token
            
        Raises:
            HTTPException: If authentication fails or other errors occur
        """
        try:
            # Find user by email
            user = self.db.query(User).filter(User.email == data.email).first()
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid email or password"
                )
            
            # Verify password
            if not pwd_context.verify(data.password, user.password):
                raise HTTPException(
                    status_code=401,
                    detail="Invalid email or password"
                )
            
            # Update last login
            user.last_login = func.now()
            
            # Clean up expired sessions for this user
            self.session_service.cleanup_expired_sessions(user.id)
            
            # Check for existing valid session
            existing_session = self.db.query(SessionModel).filter(
                and_(
                    SessionModel.user_id == user.id,
                    SessionModel.expires_at > datetime.utcnow(),
                    SessionModel.is_active == True
                )
            ).first()
            
            if existing_session:
                # Update existing session
                existing_session.last_activity = func.now()
                existing_session.ip_address = ip_address
                existing_session.user_agent = user_agent
                session_token = existing_session.token
                expires_at = existing_session.expires_at
            else:
                # Create new session
                session_token = secrets.token_urlsafe(32)
                expires_at = datetime.utcnow() + timedelta(days=30)  # 30 days session
                
                new_session = SessionModel(
                    user_id=user.id,
                    token=session_token,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    expires_at=expires_at
                )
                
                self.db.add(new_session)
            
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
                    "is_verified": user.is_verified
                },
                "session": {
                    "token": session_token,
                    "expires_at": expires_at.isoformat()
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) 