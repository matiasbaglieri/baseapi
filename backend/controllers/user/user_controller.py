from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from schemas.user import LoginRequest, RegisterRequest, ForgotPasswordRequest, ResetPasswordRequest
from core.init_db import get_db
from models.user import User
from passlib.context import CryptContext
from sqlalchemy import func
from tasks.email_tasks import send_email

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/login")
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        # Find user by email
        user = db.query(User).filter(User.email == data.email).first()
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
        db.commit()
        
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

@router.post("/register")
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == data.email).first()
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
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
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