from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    subscription_type = Column(String(50), nullable=False)  # e.g., 'monthly', 'yearly', 'lifetime'
    currency = Column(String(3), nullable=False)  # e.g., 'USD', 'EUR'
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subscription_users = relationship("SubscriptionUser", back_populates="subscription")
    payments = relationship("Payment", back_populates="subscription")

    def __repr__(self):
        return f"<Subscription {self.name} ({self.subscription_type})>" 