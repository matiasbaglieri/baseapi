from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from core.init_db import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id", ondelete="SET NULL"), nullable=True)
    subscription_user_id = Column(Integer, ForeignKey("subscription_users.id", ondelete="SET NULL"), nullable=True)
    amount = Column(Float, nullable=True)
    currency = Column(String(3), default="USD")
    status = Column(String(50), nullable=False, default="pending")
    stripe_payment_intent_id = Column(String(255), nullable=True)
    stripe_customer_id = Column(String(255), nullable=True)
    payment_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Use string reference for relationship to avoid circular imports
    user = relationship("User", back_populates="payments", lazy="joined")
    subscription = relationship("Subscription", back_populates="payments", lazy="joined")
    subscription_user = relationship("SubscriptionUser", back_populates="payments", lazy="joined")

    def __repr__(self):
        return f"<Payment {self.id} - {self.user_id} ({self.status})>" 