from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from models.session import Session as SessionModel
from passlib.context import CryptContext
from sqlalchemy import func, and_
from tasks.email_tasks import send_email
from schemas.user import RegisterRequest
from core.jwt import JWTManager
from core.roles import UserRole
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from core.logger import logger
from services.country.country_service import CountryService
from core.config import settings
from services.city.city_service import CityService

# Load environment variables
load_dotenv()

# Get refresh token expiration days from environment
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterService:
    def __init__(self, db: Session):
        self.db = db
        self.country_service = CountryService(db)
        self.city_service = CityService(db)

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
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            
            # Validate country if provided
            country = None
            if data.country or data.country_code:
                country = self.country_service.validate_country(
                    country_name=data.country,
                    country_code=data.country_code
                )
            if not country:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid country"
                )

            # Validate city if provided
            city = None
            if data.city and country:
                city = self.city_service.validate_city(
                    city_name=data.city,
                    country_id=country.country_id
                )
            
            # Create new user
            new_user = User(
                email=data.email,
                first_name=data.first_name,
                last_name=data.last_name,
                role=UserRole.USER.value,  # Default role
                country_id=country.id if country else None,
                city_id=city.id if city else None,
                language=data.language or 'en',  # Use provided language or default to 'en'
                subscription='FREE'
            )
            new_user.set_password(data.password)
            
            self.db.add(new_user)
            self.db.flush()  # Flush to get the user ID
            
            # Create JWT tokens
            tokens = JWTManager.create_tokens_response(
                user_id=new_user.id,
                email=new_user.email,
                role=UserRole.USER
            )
            
            # Calculate expiration time
            expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            
            # Create new session
            new_session = SessionModel(
                user_id=new_user.id,
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                token_type="bearer",
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
                    "role": new_user.role,
                    "country": country.name if country else None,
                    "country_code": country.iso2 if country else None,
                    "city": city.name if city else None,
                    "language": new_user.language
                },
                "tokens": {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                    "token_type": "bearer",
                    "expires_in": 900  # 15 minutes in seconds
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error registering user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while registering user"
            ) 