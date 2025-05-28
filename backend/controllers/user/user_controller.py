from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request, status, Header
from sqlalchemy.orm import Session
from schemas.user import LoginRequest, RegisterRequest, ForgotPasswordRequest, ResetPasswordRequest, RefreshTokenRequest, UserCreate, UserUpdate, UserResponse
from core.database import get_db
from models.user import User
from passlib.context import CryptContext
from sqlalchemy import func, and_
from services.user import RegisterService, LoginService, PasswordResetService, UserService
from services.jwt.refresh_token_service import RefreshTokenService
from core.jwt import JWTManager
from models.session import Session as SessionModel
from datetime import datetime, timedelta
from controllers.base import BaseController
from core.roles import UserRole
from core.logger import logger
from typing import Optional

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserController(BaseController[User]):
    def __init__(self):
        super().__init__(User)
        self.router = APIRouter(prefix="/users", tags=["users"])
        self.setup_routes()

    def setup_routes(self):
        @self.router.get("/me", response_model=UserResponse)
        async def get_current_user(
            authorization: Optional[str] = Header(None),
            db: Session = Depends(get_db)
        ):
            """
            Get current user data using JWT token.
            """
            if not authorization or not authorization.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header"
                )
            
            access_token = authorization.split(" ")[1]
            user_service = UserService(db)
            return user_service.get_current_user(access_token)

        @self.router.put("/me", response_model=UserResponse)
        async def update_user_profile(
            update_data: UserUpdate,
            authorization: Optional[str] = Header(None),
            db: Session = Depends(get_db)
        ):
            """
            Update current user's profile information.
            """
            if not authorization or not authorization.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header"
                )
            
            access_token = authorization.split(" ")[1]
            user_service = UserService(db)
            
            # First get the current user to ensure authentication
            current_user = user_service.get_current_user(access_token)
            
            # Then update the user's profile
            updated_user = user_service.update_user_profile(current_user.id, update_data)
            return updated_user

        @self.router.post("/login")
        async def login(
            request: Request,
            data: LoginRequest,
            db: Session = Depends(get_db)
        ):
            """
            Login a user and return JWT tokens.
            """
            login_service = LoginService(db)
            return login_service.login_user(
                data=data,
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent")
            )

        @self.router.post("/refresh-token")
        async def refresh_token(
            request: Request,
            data: RefreshTokenRequest,
            db: Session = Depends(get_db)
        ):
            """
            Refresh the access token using a refresh token.
            Creates a new session if the current one is expired.
            """
            refresh_token_service = RefreshTokenService(db)
            return refresh_token_service.refresh_token(
                refresh_token=data.refresh_token,
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent")
            )

        @self.router.post("/register")
        async def register(request: Request, data: RegisterRequest, db: Session = Depends(get_db)):
            """
            Register a new user.
            """
            register_service = RegisterService(db)
            return register_service.register_user(
                data=data,
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent")
            )

        @self.router.post("/forgot-password")
        async def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
            """
            Request a password reset.
            """
            password_reset_service = PasswordResetService(db)
            return password_reset_service.create_password_reset(data.email)

        @self.router.post("/reset-password")
        async def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
            """
            Reset password using a valid token.
            """
            password_reset_service = PasswordResetService(db)
            return password_reset_service.reset_password(data.token, data.new_password)

# Create router instance
user_controller = UserController()
router = user_controller.router 