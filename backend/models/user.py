from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.init_db import Base
from core.roles import UserRole
from passlib.context import CryptContext
from datetime import datetime
import sqlalchemy as sa

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole, values_callable=lambda x: [e.value for e in x]), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_blocked = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    retry_count = Column(Integer, default=0)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP'))
    last_login = Column(DateTime, nullable=True)
    profile_picture = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    language = Column(String(10), default="en")
    address = Column(Text, nullable=True)
    postal_code = Column(String(20), nullable=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    subscription = Column(String(50), nullable=True)

    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan", lazy="joined")
    password_resets = relationship("PasswordReset", back_populates="user", cascade="all, delete-orphan", lazy="joined")
    email_verifications = relationship("EmailVerification", back_populates="user", cascade="all, delete-orphan", lazy="joined")
    country = relationship("Country", back_populates="users")
    city = relationship("City", back_populates="users")
    subscription_users = relationship("SubscriptionUser", back_populates="user", cascade="all, delete-orphan", lazy="joined")
    subscriptions = relationship("SubscriptionUser", back_populates="user", cascade="all, delete-orphan", lazy="joined", overlaps="subscription_users")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan", lazy="joined")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan", lazy="joined")

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