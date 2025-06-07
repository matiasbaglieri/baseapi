from sqlalchemy.orm import Session
from models.payment import Payment
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload
import stripe
from datetime import datetime
from core.config import settings

class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        stripe.api_key = settings.STRIPE_API_KEY

    def get_user_payments(self, user_id: int, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
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

    def create_payment_transaction(
        self,
        user_id: int,
        amount: float,
        currency: str,
        stripe_customer_id: str,
        description: str = None
    ) -> Dict[str, Any]:
        """
        Create a new payment transaction using Stripe
        """
        try:
            # Create Stripe payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency.lower(),
                customer=stripe_customer_id,
                description=description,
                payment_method_types=['card']
            )

            # Create payment record
            payment = Payment(
                user_id=user_id,
                amount=amount,
                currency=currency,
                payment_type="TX",
                payment_method="stripe",
                status="pending",
                date=datetime.utcnow(),
                stripe_payment_intent_id=payment_intent.id,
                data_json={
                    "description": description,
                    "stripe_customer_id": stripe_customer_id,
                    "client_secret": payment_intent.client_secret
                }
            )
            
            self.db.add(payment)
            self.db.commit()
            self.db.refresh(payment)

            return {
                "payment": payment,
                "client_secret": payment_intent.client_secret
            }

        except stripe.error.StripeError as e:
            self.db.rollback()
            raise ValueError(f"Stripe error: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error creating payment: {str(e)}")
