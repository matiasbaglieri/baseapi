from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User
from passlib.context import CryptContext
from sqlalchemy import func
from tasks.email_tasks import send_email
from schemas.user import LoginRequest

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginService:
    def __init__(self, db: Session):
        self.db = db

    def login_user(self, data: LoginRequest) -> dict:
        """
        Authenticate and login a user.
        
        Args:
            data (LoginRequest): User login credentials
            
        Returns:
            dict: Login response with user data
            
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
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) 