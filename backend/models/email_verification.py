from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.init_db import Base
from datetime import datetime
import sqlalchemy as sa

class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP'))

    # Use string reference for relationship to avoid circular imports
    user = relationship("User", back_populates="email_verifications", lazy="joined")

    def __repr__(self):
        return f"<EmailVerification {self.id} - {self.user_id}>" 