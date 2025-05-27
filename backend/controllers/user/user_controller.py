from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.user import LoginRequest, RegisterRequest, ForgotPasswordRequest, ResetPasswordRequest
from core.init_db import get_db
from models.user import User
from passlib.context import CryptContext
from sqlalchemy import func

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
async def register(data: RegisterRequest):
    try:
        # Dummy implementation
        return {
            "message": f"User {data.email} first name {data.first_name} last name {data.last_name} registered.",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest):
    try:
        # Dummy implementation
        return {
            "message": f"Password reset link sent to {data.email}.",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest):
    try:
        # Dummy implementation
        return {
            "message": "Password has been reset.",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 