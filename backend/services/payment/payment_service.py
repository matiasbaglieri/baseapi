from sqlalchemy.orm import Session
from models.payment import Payment
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_payments(self, user_id: int, skip: int = 0, limit: int = 10):
        """
        Get all payments for a user with pagination and related data
        """
        try:
            # Query payments with related subscription and subscription_user data
            query = self.db.query(Payment)\
                .options(
                    joinedload(Payment.subscription),
                    joinedload(Payment.subscription_user)
                )\
                .filter(Payment.user_id == user_id)\
                .order_by(Payment.date.desc())

            # Get total count for pagination
            total_count = query.count()

            # Apply pagination
            payments = query.offset(skip).limit(limit).all()

            return {
                "total": total_count,
                "items": payments,
                "page": skip // limit + 1,
                "pages": (total_count + limit - 1) // limit
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving payments: {str(e)}"
            )
