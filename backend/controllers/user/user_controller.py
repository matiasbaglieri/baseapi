from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from schemas.user import LoginRequest, RegisterRequest, ForgotPasswordRequest, ResetPasswordRequest
from core.init_db import get_db
from models.user import User
from passlib.context import CryptContext
from sqlalchemy import func
from tasks.email_tasks import send_email
from services.user import RegisterService, LoginService, PasswordResetService

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/login")
async def login(request: Request, data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate and login a user.
    """
    login_service = LoginService(db)
    return login_service.login_user(
        data=data,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )

@router.post("/register")
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

@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Request a password reset.
    """
    password_reset_service = PasswordResetService(db)
    return password_reset_service.create_password_reset(data.email)

@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset password using a valid token.
    """
    password_reset_service = PasswordResetService(db)
    return password_reset_service.reset_password(data.token, data.new_password) 