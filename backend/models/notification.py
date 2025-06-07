from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.init_db import Base
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    is_read = Column(Boolean, default=False)
    action = Column(String(50), nullable=False)  # e.g., 'payment', 'subscription', 'system'
    data_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.id} - {self.user_id} ({self.action})>" 