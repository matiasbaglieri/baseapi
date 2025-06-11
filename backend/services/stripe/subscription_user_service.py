from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.subscription import Subscription
from models.subscription_user import SubscriptionUser
from models.payment import Payment
from schemas.subscription import SubscriptionUserCreate
from datetime import datetime, timedelta
from services.stripe.subscription_service import StripeSubscriptionService
from core.config import settings
from core.logger import logger
from sqlalchemy import or_

class SubscriptionUserService:
    def __init__(self, db: Session):
        self.db = db
        self.subscription_service = StripeSubscriptionService(db, settings.STRIPE_API_KEY)

    async def create_user_subscription(self, user_id: int, subscription_data: SubscriptionUserCreate):
        """
        Create a new subscription for a user with associated payment.
        If payment_type is bank_check, creates subscription without Stripe.
        If subscription exists and is the same, returns it.
        If subscription exists but is different, cancels it and its pending payments.
        """
        try:
            # Get subscription
            subscription = self.db.query(Subscription).filter(
                Subscription.id == subscription_data.subscription_id
            ).first()

            if not subscription:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subscription not found"
                )

            # Check for existing subscription with pending or active status
            existing_subscription = self.db.query(SubscriptionUser).filter(
                SubscriptionUser.user_id == user_id,
                or_(
                    SubscriptionUser.status == "pending",
                    SubscriptionUser.status == "active"
                )
            ).first()

            if existing_subscription:
                # If subscription exists and is the same, return it
                if existing_subscription.subscription_id == subscription_data.subscription_id:
                    # Get the associated payment
                    payment = self.db.query(Payment).filter(
                        Payment.subscription_user_id == existing_subscription.id,
                        Payment.status == "pending"
                    ).first()
                    
                    return {
                        "subscription_user": existing_subscription,
                        "payment": payment,
                        "message": "Subscription already exists"
                    }
                
                # Cancel existing subscription and its pending payments
                existing_subscription.status = "cancelled"
                existing_subscription.updated_at = datetime.utcnow()
                
                # Cancel pending payments
                pending_payments = self.db.query(Payment).filter(
                    Payment.subscription_user_id == existing_subscription.id,
                    Payment.status == "pending"
                ).all()
                
                for payment in pending_payments:
                    payment.status = "cancelled"
                    payment.updated_at = datetime.utcnow()

            # Create new subscription user
            subscription_user = SubscriptionUser(
                user_id=user_id,
                subscription_id=subscription_data.subscription_id,
                status="pending",
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=subscription.duration),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            self.db.add(subscription_user)
            self.db.flush()  # Flush to get the ID

            # Handle payment based on payment type
            payment = None
            if subscription_data.payment_type == "bank_check":
                # Create payment without Stripe
                payment = Payment(
                    user_id=user_id,
                    subscription_id=subscription_data.subscription_id,
                    subscription_user_id=subscription_user.id,
                    amount=subscription_data.amount or subscription.price,
                    currency=subscription_data.currency or subscription.currency,
                    status="pending",
                    payment_type="bank_check",
                    payment_method="bank_check",
                    payment_data=subscription_data.payment_data or {},
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    date=datetime.utcnow()
                )
                self.db.add(payment)
            else:
                # Use Stripe for other payment types
                stripe_result = await self.subscription_service.create_subscription(
                    user_id=user_id,
                    subscription_id=subscription_data.subscription_id,
                    payment_method_id=subscription_data.payment_method_id
                )
                
                # Update subscription user with Stripe data
                subscription_user.stripe_subscription_id = stripe_result.get("stripe_subscription_id")
                subscription_user.stripe_customer_id = stripe_result.get("stripe_customer_id")
                subscription_user.client_secret = stripe_result.get("client_secret")
                subscription_user.subscription_data = stripe_result.get("subscription_data", {})
                
                # Get the payment created by Stripe
                payment = self.db.query(Payment).filter(
                    Payment.subscription_user_id == subscription_user.id,
                    Payment.status == "pending"
                ).first()
            
            # Commit all changes
            self.db.commit()
            
            return {
                "subscription_user": subscription_user,
                "payment": payment,
                "message": "Subscription created successfully"
            }

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating subscription: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating subscription: {str(e)}"
            )
