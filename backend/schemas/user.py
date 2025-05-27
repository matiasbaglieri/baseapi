from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional

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