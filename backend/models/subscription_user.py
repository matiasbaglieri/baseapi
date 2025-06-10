from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from core.init_db  import Base
from datetime import datetime

class SubscriptionUser(Base):
    __tablename__ = "subscription_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    status = Column(String(20), nullable=False)  # e.g., 'active', 'cancelled', 'expired'
    data_json = Column(JSON, nullable=True)  # Additional subscription data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    start_date = Column(DateTime, nullable=True) 
    end_date = Column(DateTime, nullable=True)  
    stripe_subscription_id = Column(String(100), nullable=True)
    client_secret = Column(String(500), nullable=True)  # Stripe client secret if applicable
    stripe_customer_id = Column(String(100), nullable=True)
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    subscription = relationship("Subscription", back_populates="subscription_users")
    payments = relationship("Payment", back_populates="subscription_user")

    def __repr__(self):
        return f"<SubscriptionUser {self.user_id} - {self.subscription_id} ({self.status})>" 