from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User
from models.session import Session as SessionModel
from passlib.context import CryptContext
from sqlalchemy import func
from tasks.email_tasks import send_email
from schemas.user import RegisterRequest
from core.jwt import JWTManager
from core.roles import UserRole
from datetime import datetime, timedelta
import secrets

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, data: RegisterRequest, ip_address: str = None, user_agent: str = None) -> dict:
        """
        Register a new user.
        
        Args:
            data (RegisterRequest): User registration data
            ip_address (str, optional): IP address of the client
            user_agent (str, optional): User agent string of the client
            
        Returns:
            dict: Registration response with user data and JWT tokens
            
        Raises:
            HTTPException: If registration fails or other errors occur
        """
        try:
            # Check if user already exists
            existing_user = self.db.query(User).filter(User.email == data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )
            
            # Hash password
            hashed_password = pwd_context.hash(data.password)
            
            # Create new user
            new_user = User(
                email=data.email,
                password=hashed_password,
                first_name=data.first_name,
                last_name=data.last_name,
                role=UserRole.USER
            )
            
            self.db.add(new_user)
            self.db.flush()  # Flush to get the user ID
            # Create JWT tokens
            tokens = JWTManager.create_tokens_response(
                user_id=new_user.id,
                email=new_user.email,
                role=UserRole.USER
            )
            # Create new session
            expires_at = datetime.utcnow() + timedelta(days=30)  # 30 days session
            
            new_session = SessionModel(
                user_id=new_user.id,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                token_type=tokens["token_type"],
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
                    "last_name": new_user.last_name,
                    "is_verified": new_user.is_verified,
                    "role": new_user.role
                },
                "tokens": tokens
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) 