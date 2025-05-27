from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request, status
from sqlalchemy.orm import Session
from schemas.user import LoginRequest, RegisterRequest, ForgotPasswordRequest, ResetPasswordRequest, RefreshTokenRequest
from core.database import get_db
from models.user import User
from passlib.context import CryptContext
from sqlalchemy import func, and_
from tasks.email_tasks import send_email
from services.user import RegisterService, LoginService, PasswordResetService
from core.jwt import JWTManager
from models.session import Session as SessionModel
from datetime import datetime, timedelta
from controllers.base import BaseController
from core.roles import UserRole
from core.logger import logger

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserController(BaseController[User]):
    def __init__(self):
        super().__init__(User)
        self.router = APIRouter(prefix="/users", tags=["users"])
        self.setup_routes()

    def setup_routes(self):
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
            try:
                # Verify the refresh token
                payload = JWTManager.verify_token(data.refresh_token)
                user_id = int(payload["sub"])
                email = payload["email"]
                try:
                    role = UserRole(payload["role"])  # Convert string to UserRole enum
                except ValueError as e:
                    logger.warning(f"Could not parse role '{payload.get('role')}', using default value: {str(e)}")
                    role = UserRole.USER  # Default to USER role if parsing fails

                # Check for existing valid session
                existing_session = db.query(SessionModel).filter(
                    and_(
                        SessionModel.user_id == user_id,
                        SessionModel.refresh_token == data.refresh_token,
                        SessionModel.expires_at > datetime.utcnow(),
                        SessionModel.is_active == True
                    )
                ).first()

                if existing_session:
                    # Update existing session with new tokens
                    tokens = JWTManager.create_tokens_response(
                        user_id=user_id,
                        email=email,
                        role=role
                    )
                    
                    existing_session.access_token = tokens["access_token"]
                    existing_session.refresh_token = tokens["refresh_token"]
                    existing_session.last_activity = datetime.utcnow()
                    existing_session.ip_address = request.client.host
                    existing_session.user_agent = request.headers.get("user-agent")
                    
                    access_token = tokens["access_token"]
                    refresh_token = tokens["refresh_token"]
                else:
                    # Create new session with new tokens
                    tokens = JWTManager.create_tokens_response(
                        user_id=user_id,
                        email=email,
                        role=role
                    )
                    
                    new_session = SessionModel(
                        user_id=user_id,
                        access_token=tokens["access_token"],
                        refresh_token=tokens["refresh_token"],
                        token_type="bearer",
                        ip_address=request.client.host,
                        user_agent=request.headers.get("user-agent"),
                        expires_at=datetime.utcnow() + timedelta(days=7)
                    )
                    
                    db.add(new_session)
                    access_token = tokens["access_token"]
                    refresh_token = tokens["refresh_token"]

                db.commit()

                return {
                    "message": "Token refreshed successfully",
                    "status": "success",
                    "tokens": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "token_type": "bearer",
                        "expires_in": 900  # 15 minutes in seconds
                    }
                }

            except Exception as e:
                logger.error(f"Token refresh failed: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=str(e)
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