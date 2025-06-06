from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.subscription import Subscription
from models.subscription_user import SubscriptionUser
from models.payment import Payment
from schemas.subscription import SubscriptionUserCreate
from datetime import datetime
from services.stripe.subscription_service import StripeSubscriptionService

class SubscriptionUserService:
    def __init__(self, db: Session, stripe_api_key: str):
        self.db = db
        self.subscription_service = StripeSubscriptionService(db, stripe_api_key)

    async def create_user_subscription(self, user_id: int, subscription_data: SubscriptionUserCreate):
        """
        Create a new subscription for a user with associated payment
        """
        try:
            # Get the subscription
            subscription = self.subscription_service.get_subscription(subscription_data.subscription_id)
            if not subscription:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subscription not found"
                )

            # Check for existing active subscription
            existing_subscription = self.db.query(SubscriptionUser).filter(
                SubscriptionUser.user_id == user_id,
                SubscriptionUser.subscription_id == subscription.id,
                SubscriptionUser.status == "active"
            ).first()

            if existing_subscription:
                subscription_user = existing_subscription
            else:
                # Create new subscription user record
                subscription_user = SubscriptionUser(
                    user_id=user_id,
                    subscription_id=subscription.id,
                    status="active",
                    start_date=datetime.utcnow(),
                    data_json=subscription_data.dict()
                )
                self.db.add(subscription_user)
                self.db.flush()  # Get subscription_user ID without committing
            
            # Create payment record
            payment = Payment(
                user_id=user_id,
                subscription_id=subscription.id,
                subscription_user_id=subscription_user.id,
                amount=subscription_data.amount,
                currency=subscription_data.currency,
                payment_method=subscription_data.payment_method,
                payment_type="SUBSCRIPTION",
                date=datetime.utcnow(),
                status="pending"  # Will be updated after Stripe confirmation
            )
            self.db.add(payment)
            self.db.flush()  # Get payment ID without committing
            
            # Commit the transaction
            self.db.commit()
            self.db.refresh(subscription_user)
            self.db.refresh(payment)

            return {
                "subscription_user": subscription_user,
                "payment": payment,
                "subscription": subscription
            }

        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating subscription: {str(e)}"
            )
