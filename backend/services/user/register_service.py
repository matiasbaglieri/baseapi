from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User
from models.session import Session as SessionModel
from passlib.context import CryptContext
from sqlalchemy import func
from tasks.email_tasks import send_email
from schemas.user import RegisterRequest
from .session_service import SessionService
import secrets
from datetime import datetime, timedelta

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterService:
    def __init__(self, db: Session):
        self.db = db
        self.session_service = SessionService(db)

    def register_user(self, data: RegisterRequest, ip_address: str = None, user_agent: str = None) -> dict:
        """
        Register a new user.
        
        Args:
            data (RegisterRequest): User registration data
            ip_address (str, optional): IP address of the client
            user_agent (str, optional): User agent string of the client
            
        Returns:
            dict: Registration response with user data and session token
            
        Raises:
            HTTPException: If email already exists or other errors occur
        """
        try:
            # Check if user already exists
            existing_user = self.db.query(User).filter(User.email == data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )
            
            # Create new user
            hashed_password = pwd_context.hash(data.password)
            new_user = User(
                email=data.email,
                password=hashed_password,
                first_name=data.first_name,
                last_name=data.last_name
            )
            
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            
            # Clean up any existing expired sessions for this user
            self.session_service.cleanup_expired_sessions(new_user.id)
            
            # Create new session
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(days=30)  # 30 days session
            
            new_session = SessionModel(
                user_id=new_user.id,
                token=session_token,
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=expires_at
            )
            
            self.db.add(new_session)
            self.db.commit()
            
            # Send welcome email asynchronously
            send_email.delay(
                to_email=new_user.email,
                subject="Welcome to Our Platform!",
                body=f"Welcome {new_user.first_name}! Thank you for registering."
            )
            
            return {
                "message": "Registration successful",
                "status": "success",
                "user": {
                    "id": new_user.id,
                    "email": new_user.email,
                    "first_name": new_user.first_name,
                    "last_name": new_user.last_name
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