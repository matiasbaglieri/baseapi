from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional
from datetime import datetime
from core.roles import UserRole

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
    first_name: constr(min_length=2, max_length=100) = Field(..., description="User's first name")
    last_name: constr(min_length=2, max_length=100) = Field(..., description="User's last name")
    country_id: Optional[int] = Field(None, description="ID of the user's country")
    city_id: Optional[int] = Field(None, description="ID of the user's city")
    language: Optional[str] = Field('en', description="User's preferred language (ISO 639-2 code)")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword",
                "first_name": "John",
                "last_name": "Doe",
                "country_id": 1,
                "city_id": 1,
                "language": "en"
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    profile_picture: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    is_verified: bool
    role: UserRole
    country_id: Optional[int] = None
    city_id: Optional[int] = None
    language: str = 'en'

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

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class RegisterResponse(BaseModel):
    message: str
    status: str
    user: UserResponse
    tokens: TokenResponse 