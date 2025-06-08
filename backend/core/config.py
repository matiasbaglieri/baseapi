import os
from dotenv import load_dotenv
from datetime import timedelta
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional, Dict, Any, List
from functools import lru_cache

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # Server settings
    HOST: str = Field(
        default="0.0.0.0",
        description="Server host"
    )
    PORT: int = Field(
        default=8000,
        description="Server port"
    )
    STRIPE_API_KEY: str = Field(
        default="your_stripe_secret_key",
        description="Stripe api key"
    )
    # Development settings
    DEV_MODE: bool = Field(
        default=False,
        description="Development mode flag"
    )

    # Database settings
    MYSQL_USER: str = Field(
        default="root",
        description="MySQL username"
    )
    MYSQL_PASSWORD: str = Field(
        default="",
        description="MySQL password"
    )
    MYSQL_HOST: str = Field(
        default="localhost",
        description="MySQL host"
    )
    MYSQL_PORT: str = Field(
        default="3306",
        description="MySQL port"
    )
    MYSQL_DATABASE: str = Field(
        default="baseapi",
        description="MySQL database name"
    )
    MYSQL_ROOT_PASSWORD: str = Field(
        default="toor",
        description="MySQL root password"
    )
    DATABASE_URL: Optional[str] = None
    
    # CORS settings
    CORS_ORIGINS: List[str] = Field(
        default=["*"],
        description="CORS origins"
    )
    CORS_CREDENTIALS: bool = Field(
        default=True,
        description="CORS credentials"
    )
    CORS_METHODS: List[str] = Field(
        default=["*"],
        description="CORS methods"
    )
    CORS_HEADERS: List[str] = Field(
        default=["*"],
        description="CORS headers"
    )
    
    # Celery settings
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Celery broker URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/0",
        description="Celery result backend"
    )
    
    # Email settings
    SMTP_TLS: bool = Field(
        default=True,
        description="SMTP TLS"
    )
    SMTP_PORT: int = Field(
        default=587,
        description="SMTP port"
    )
    SMTP_HOST: str = Field(
        default="",
        description="SMTP host"
    )
    SMTP_USER: str = Field(
        default="",
        description="SMTP user"
    )
    SMTP_PASSWORD: str = Field(
        default="",
        description="SMTP password"
    )
    EMAILS_FROM_EMAIL: str = Field(
        default="",
        description="From email"
    )
    EMAILS_FROM_NAME: str = Field(
        default="",
        description="From name"
    )
    
    # Session settings
    SESSION_EXPIRY_DAYS: int = Field(
        default=7,
        description="Session expiry days"
    )
    
    # Security settings
    SECRET_KEY: str = Field(
        default="your-secret-key",
        description="Secret key"
    )
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=["*"],
        description="Backend CORS origins"
    )
    
    # API settings
    API_V1_STR: str = Field(
        default="/api/v1",
        description="API version string"
    )
    PROJECT_NAME: str = Field(
        default="BaseAPI",
        description="Project name"
    )
    
    # JWT settings
    JWT_SECRET_KEY: str = Field(
        default="your-jwt-secret-key",
        description="JWT secret key"
    )
    JWT_ALGORITHM: str = Field(
        default="HS256",
        description="JWT algorithm"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=15,
        description="Access token expiry minutes"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token expiry days"
    )
    JWT_ISSUER: str = Field(
        default="baseapi",
        description="JWT issuer"
    )
    JWT_AUDIENCE: str = Field(
        default="baseapi",
        description="JWT audience"
    )
    JWT_LEEWAY: int = Field(
        default=0,
        description="JWT leeway"
    )
    JWT_TOKEN_TYPE_ACCESS: str = Field(
        default="access",
        description="JWT access token type"
    )
    JWT_TOKEN_TYPE_REFRESH: str = Field(
        default="refresh",
        description="JWT refresh token type"
    )

    # Mailgun Settings
    MAILGUN_API_KEY: str
    MAILGUN_DOMAIN: str
    MAILGUN_FROM_EMAIL: str = "noreply@your-domain.com"

    # Redis settings
    REDIS_URL: str

    @property
    def JWT_ACCESS_TOKEN_EXPIRE(self) -> timedelta:
        """Get access token expiration time."""
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def JWT_REFRESH_TOKEN_EXPIRE(self) -> timedelta:
        """Get refresh token expiration time."""
        return timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Frontend settings
    FRONTEND_URL: str = Field(
        default="http://localhost:3000",
        description="Frontend URL"
    )

    @validator("CORS_ORIGINS", "CORS_METHODS", "CORS_HEADERS", "BACKEND_CORS_ORIGINS", pre=True)
    def parse_list(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.strip("[]").split(",")]
        return v

    @validator("DEV_MODE", pre=True)
    def parse_bool(cls, v):
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes")
        return bool(v)

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 