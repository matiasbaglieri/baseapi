from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User
from passlib.context import CryptContext
from tasks.email_tasks import send_email
from schemas.user import RegisterRequest

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, data: RegisterRequest) -> dict:
        """
        Register a new user.
        
        Args:
            data (RegisterRequest): User registration data
            
        Returns:
            dict: Registration response with user data
            
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
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) 