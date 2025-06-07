from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.init_db  import Base
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
    payment_method = Column(String(50), nullable=False)  # e.g., 'stripe', 'paypal'
    stripe_payment_intent_id = Column(String(100), nullable=True) 
    data_json = Column(JSON, nullable=True)  # For Stripe payments
    # Relationships
    user = relationship("User", back_populates="payments")
    subscription = relationship("Subscription", back_populates="payments")
    subscription_user = relationship("SubscriptionUser", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.id} - {self.user_id} ({self.status})>" 