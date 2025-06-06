from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.subscription import Subscription
from models.subscription_user import SubscriptionUser
from models.payment import Payment
from schemas.subscription import SubscriptionUserCreate
from typing import List, Optional
import stripe
from datetime import datetime
from fastapi import HTTPException, status

class StripeSubscriptionService:
    def __init__(self, db: Session, stripe_api_key: str):
        self.db = db
        stripe.api_key = stripe_api_key

    def create_subscription(self, name: str, subscription_type: str, currency: str, amount: float) -> Subscription:
        # Create Stripe product
        stripe_product = stripe.Product.create(
            name=name,
            description=f"{name} subscription plan"
        )

        # Create Stripe price
        stripe_price = stripe.Price.create(
            product=stripe_product.id,
            unit_amount=int(amount * 100),  # Convert to cents
            currency=currency.lower(),
            recurring={
                "interval": subscription_type
            }
        )

        # Create local subscription
        subscription = Subscription(
            name=name,
            subscription_type=subscription_type,
            currency=currency,
            amount=amount,
            stripe_product_id=stripe_product.id,
            stripe_price_id=stripe_price.id
        )
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        return subscription

    def get_subscription(self, subscription_id: int) -> Optional[Subscription]:
        return self.db.query(Subscription).filter(Subscription.id == subscription_id).first()

    def get_all_subscriptions(self) -> List[Subscription]:
        return self.db.query(Subscription).all()

    def init_subscriptions(self) -> List[Subscription]:
        """Initialize default subscriptions if they don't exist"""
        existing_subscriptions = self.get_all_subscriptions()
        if existing_subscriptions:
            return existing_subscriptions

        # Create PRO subscription
        pro_subscription = self.create_subscription(
            name="PRO",
            subscription_type="monthly",
            currency="USD",
            amount=25.00
        )

        # Create CORPORATE subscription
        corporate_subscription = self.create_subscription(
            name="CORPORATE",
            subscription_type="monthly",
            currency="USD",
            amount=100.00
        )

        return [pro_subscription, corporate_subscription]

    def create_customer_subscription(self, user_id: int, subscription_id: int, stripe_customer_id: str) -> dict:
        """Create a subscription for a customer in Stripe"""
        subscription = self.get_subscription(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")

        # Create Stripe subscription
        stripe_subscription = stripe.Subscription.create(
            customer=stripe_customer_id,
            items=[{"price": subscription.stripe_price_id}],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent']
        )

        return {
            "subscription_id": stripe_subscription.id,
            "client_secret": stripe_subscription.latest_invoice.payment_intent.client_secret
        }

    def cancel_subscription(self, stripe_subscription_id: str) -> dict:
        """Cancel a Stripe subscription"""
        return stripe.Subscription.delete(stripe_subscription_id)

    def get_subscription_status(self, stripe_subscription_id: str) -> dict:
        """Get the status of a Stripe subscription"""
        return stripe.Subscription.retrieve(stripe_subscription_id)