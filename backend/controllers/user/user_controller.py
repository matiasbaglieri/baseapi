from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from schemas.user import LoginRequest, RegisterRequest, ForgotPasswordRequest, ResetPasswordRequest
from core.init_db import get_db
from models.user import User
from passlib.context import CryptContext
from sqlalchemy import func
from tasks.email_tasks import send_email
from services.user import RegisterService, LoginService

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
    try:
        user = db.query(User).filter(User.email == data.email).first()
        if user:
            # Send password reset email asynchronously
            send_email.delay(
                to_email=user.email,
                subject="Password Reset Request",
                body="Click the link below to reset your password."
            )
        
        # Always return success to prevent email enumeration
        return {
            "message": "If your email is registered, you will receive a password reset link.",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        # Dummy implementation
        return {
            "message": "Password has been reset.",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 