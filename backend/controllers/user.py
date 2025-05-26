from fastapi import APIRouter, HTTPException
from schemas.user import LoginRequest, RegisterRequest, ForgotPasswordRequest, ResetPasswordRequest

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/login")
async def login(data: LoginRequest):
    try:
        # Dummy implementation
        return {
            "message": f"User {data.email} logged in.",
            "status": "success"
        }
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