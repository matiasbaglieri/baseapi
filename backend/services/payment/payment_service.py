from sqlalchemy.orm import Session
from models.payment import Payment
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload
import stripe
from datetime import datetime
from core.config import settings
from services.notification.notification_service import NotificationService
import logging
from models.user import User

# Configure logger
logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        stripe.api_key = settings.STRIPE_API_KEY
        self.notification_service = NotificationService(db)


    def _convert_payment_to_dict(self, payment: Payment) -> Dict[str, Any]:
        """Convert Payment model to dictionary"""

        return {
            "id": payment.id,
            "user_id": payment.user_id,
            "subscription_id": payment.subscription_id,
            "subscription_user_id": payment.subscription_user_id,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status,
            "stripe_payment_intent_id": payment.stripe_payment_intent_id,
            "stripe_customer_id": payment.stripe_customer_id,
            "payment_method": payment.payment_method,
            "payment_type": payment.payment_type,
            "date": payment.date,
            "data_json": payment.data_json,
            "created_at": payment.created_at,
            "updated_at": payment.updated_at,
            "subscription": {
                "id": payment.subscription.id,
                "name": payment.subscription.name,
                "subscription_type": payment.subscription.subscription_type,
                "price": payment.subscription.price,
                "currency": payment.subscription.currency,
                "features": payment.subscription.features,
                "is_active": payment.subscription.is_active
            } if payment.subscription else None,
            "subscription_user": {
                "id": payment.subscription_user.id,
                "status": payment.subscription_user.status,
                "start_date": payment.subscription_user.start_date,
                "end_date": payment.subscription_user.end_date,
                "stripe_subscription_id": payment.subscription_user.stripe_subscription_id,
                "stripe_customer_id": payment.subscription_user.stripe_customer_id
            } if payment.subscription_user else None
        }

    def get_user_payments(self, user_id: int, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        """
        Get all payments for a user with pagination and related data
        """
        try:
            # Query payments with related subscription and subscription_user data
            query = self.db.query(Payment)\
                .options(
                    joinedload(Payment.subscription),
                    joinedload(Payment.subscription_user),
                    joinedload(Payment.user)
                )\
                .filter(Payment.user_id == user_id)\
                .order_by(Payment.date.desc())

            # Get total count for pagination
            total_count = query.count()

            # Apply pagination
            payments = query.offset(skip).limit(limit).all()

            # Convert payments to dictionaries
            payment_dicts = [self._convert_payment_to_dict(payment) for payment in payments]

            return {
                "total": total_count,
                "items": payment_dicts,
                "page": skip // limit + 1,
                "pages": (total_count + limit - 1) // limit
            }

        except Exception as e:
            logger.error(f"Error retrieving payments: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving payments: {str(e)}"
            )

    def _get_or_create_stripe_customer(self, user_id: int) -> str:
        """Get or create Stripe customer for user"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # Try to find existing customer
        customers = stripe.Customer.list(email=user.email, limit=1)
        if customers and customers.data:
            return customers.data[0].id

        # Create new customer
        customer = stripe.Customer.create(
            email=user.email,
            name=f"{user.first_name} {user.last_name}",
            metadata={"user_id": user.id}
        )
        return customer.id

    def create_payment_transaction(
        self,
        user_id: int,
        amount: float,
        currency: str,
        description: str = None
    ) -> Dict[str, Any]:
        """
        Create a new payment transaction using Stripe
        """
        try:
            # Get or create Stripe customer
            stripe_customer_id = self._get_or_create_stripe_customer(user_id)

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

            # Create notification for the payment
            self.notification_service.create_notification(
                user_id=user_id,
                title="payment.pending.tx",
                action="PAYMENT",
                data_json={
                    "payment_id": payment.id,
                    "amount": amount,
                    "currency": currency,
                    "description": description,
                    "stripe_payment_intent_id": payment_intent.id
                }
            )

            return {
                "payment": self._convert_payment_to_dict(payment),
                "client_secret": payment_intent.client_secret
            }

        except stripe.error.StripeError as e:
            self.db.rollback()
            raise ValueError(f"Stripe error: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error creating payment: {str(e)}")

    def find_or_create_payment_transaction(
        self,
        user_id: int,
        amount: float,
        currency: str,
        description: str = None
    ) -> Dict[str, Any]:
        """
        Find existing payment transaction or create new one
        """
        try:
            # Find existing pending payment
            existing_payment = self.db.query(Payment).filter(
                Payment.user_id == user_id,
                Payment.amount == amount,
                Payment.currency == currency,
                Payment.payment_type == "TX",
                Payment.status == "pending"
            ).first()

            if existing_payment:
                logger.info(f"Found existing payment transaction: {existing_payment.id}")
                return {
                    "payment": self._convert_payment_to_dict(existing_payment),
                    "client_secret": existing_payment.data_json.get("client_secret")
                }

            # Create new payment if none exists
            logger.info("No existing payment found, creating new transaction")
            return self.create_payment_transaction(
                user_id=user_id,
                amount=amount,
                currency=currency,
                description=description
            )

        except Exception as e:
            logger.error(f"Error in find_or_create_payment_transaction: {str(e)}")
            raise ValueError(f"Error processing payment: {str(e)}")
