from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from core.init_db import Base
from datetime import datetime

class SubscriptionUser(Base):
    __tablename__ = "subscription_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    stripe_subscription_id = Column(String(255), nullable=True)
    client_secret = Column(String(255), nullable=True)
    subscription_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default="now()")
    updated_at = Column(DateTime(timezone=True), onupdate="now()")

    # Use string reference for relationship to avoid circular imports
    user = relationship("User", back_populates="subscriptions", lazy="joined")
    subscription = relationship("Subscription", back_populates="users", lazy="joined")
    payments = relationship("Payment", back_populates="subscription_user", lazy="joined", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SubscriptionUser {self.user_id} - {self.subscription_id} ({self.status})>" 