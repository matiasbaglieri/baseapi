from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, description="User's password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password123"
            }
        }

class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: constr(min_length=8) = Field(..., description="User's password")
    first_name: str = Field(..., min_length=2, description="User's first name")
    last_name: str = Field(..., min_length=2, description="User's last name")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password123",
                "first_name": "John",
                "last_name": "Doe"
            }
        }

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="User's email address")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }

class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="Reset password token")
    new_password: constr(min_length=8) = Field(..., description="New password")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "reset-token-123",
                "new_password": "newpassword123"
            }
        }

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token")

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "refresh-token-123"
            }
        }

class EmailVerificationRequest(BaseModel):
    token: str = Field(..., description="Email verification token")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "verification-token-123"
            }
        }

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_picture: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    profile_picture: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: constr(min_length=8)
    confirm_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "your_current_password",
                "new_password": "your_new_password",
                "confirm_password": "your_new_password"
            }
        } 