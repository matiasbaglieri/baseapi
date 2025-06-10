from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.init_db import Base
from datetime import datetime

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    subscription_type = Column(String(100), nullable=False, default="month")
    currency = Column(String(3), default="USD")
    duration = Column(Integer, nullable=False)  # Duration in days
    features = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    stripe_price_id = Column(String(255), nullable=True)
    stripe_product_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Use string reference for relationship to avoid circular imports
    users = relationship("SubscriptionUser", back_populates="subscription", lazy="joined", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="subscription", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subscription {self.name}>" 