from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.init_db import Base
from core.roles import UserRole
from passlib.context import CryptContext
from datetime import datetime

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    profile_picture = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)

    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    password_resets = relationship("PasswordReset", back_populates="user", cascade="all, delete-orphan")
    email_verifications = relationship("EmailVerification", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        """
        Hash and set the user's password.
        
        Args:
            password (str): Plain text password to hash and set
        """
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """
        Verify the user's password.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        # Verify the password against the stored hash
        return pwd_context.verify(password, self.password)

    def __repr__(self):
        return f"<User {self.email}>" 