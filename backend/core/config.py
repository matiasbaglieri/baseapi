import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Celery settings
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:root@localhost/baseapi")
    
    # Email settings
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    
    # Session settings
    SESSION_EXPIRY_DAYS = int(os.getenv("SESSION_EXPIRY_DAYS", "30"))
    
    # Security settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create settings instance
settings = Settings() 