from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)
    subscription_user_id = Column(Integer, ForeignKey("subscription_users.id"), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), nullable=False)  # e.g., 'pending', 'completed', 'failed', 'refunded'
    currency = Column(String(3), nullable=False)  # e.g., 'USD', 'EUR'
    amount = Column(Float, nullable=False)
    payment_type = Column(String(50), nullable=False)  # e.g., 'SUBSCRIPTION', 'TX'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="payments")
    subscription = relationship("Subscription", back_populates="payments")
    subscription_user = relationship("SubscriptionUser", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.id} - {self.user_id} ({self.status})>" 