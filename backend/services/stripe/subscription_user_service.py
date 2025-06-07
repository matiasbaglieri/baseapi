from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.subscription import Subscription
from models.subscription_user import SubscriptionUser
from models.payment import Payment
from schemas.subscription import SubscriptionUserCreate
from datetime import datetime
from services.stripe.subscription_service import StripeSubscriptionService
from core.config import settings

class SubscriptionUserService:
    def __init__(self, db: Session):
        self.db = db
        self.subscription_service = StripeSubscriptionService(db, settings.STRIPE_API_KEY)

    async def create_user_subscription(self, user_id: int, subscription_data: SubscriptionUserCreate):
        """
        Create a new subscription for a user with associated payment
        """
        try:
            # Create subscription in Stripe and get subscription user
            stripe_result = self.subscription_service.create_customer_subscription(
                user_id=user_id,
                subscription_id=subscription_data.subscription_id,
                stripe_customer_id=subscription_data.stripe_customer_id
            )

            # Get the created subscription user
            subscription_user = self.db.query(SubscriptionUser).filter(
                SubscriptionUser.id == stripe_result["subscription_user_id"]
            ).first()

            if not subscription_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create subscription user"
                )

            return {
                "subscription_user": subscription_user,
                "client_secret": stripe_result["client_secret"],
                "stripe_subscription_id": stripe_result["subscription_id"]
            }

        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating subscription: {str(e)}"
            )
