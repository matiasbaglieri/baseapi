from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.subscription import Subscription
from models.subscription_user import SubscriptionUser
from models.payment import Payment
from schemas.subscription import SubscriptionUserCreate
from typing import List, Optional, Dict, Any
import stripe
from datetime import datetime
from fastapi import HTTPException, status
from core.config import settings
from services.notification.notification_service import NotificationService

class StripeSubscriptionService:
    def __init__(self, db: Session):
        self.db = db
        stripe.api_key = settings.STRIPE_API_KEY
        self.notification_service = NotificationService(db)

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

        # Get existing active subscriptions for the user
        existing_active_subscriptions = self.db.query(SubscriptionUser).filter(
            SubscriptionUser.user_id == user_id,
            SubscriptionUser.status == "active"
        ).all()

        # Cancel existing subscriptions
        for existing_sub in existing_active_subscriptions:
            self.cancel_subscription(existing_sub.id)

        # Create Stripe subscription
        stripe_subscription = stripe.Subscription.create(
            customer=stripe_customer_id,
            items=[{"price": subscription.stripe_price_id}],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent']
        )

        # Check for existing subscription user
        existing_subscription = self.db.query(SubscriptionUser).filter(
            SubscriptionUser.user_id == user_id,
            SubscriptionUser.subscription_id == subscription_id,
            SubscriptionUser.status == "active"
        ).first()

        if existing_subscription:
            # Update existing subscription
            existing_subscription.stripe_subscription_id = stripe_subscription.id
            existing_subscription.client_secret = stripe_subscription.latest_invoice.payment_intent.client_secret
            subscription_user = existing_subscription
        else:
            # Create new subscription user record
            subscription_user = SubscriptionUser(
                user_id=user_id,
                subscription_id=subscription_id,
                status="active",
                start_date=datetime.utcnow(),
                stripe_subscription_id=stripe_subscription.id,
                client_secret=stripe_subscription.latest_invoice.payment_intent.client_secret
            )
            self.db.add(subscription_user)

        self.db.flush()  # Get subscription_user ID without committing

        # Create payment record
        payment = Payment(
            user_id=user_id,
            subscription_id=subscription_id,
            subscription_user_id=subscription_user.id,
            amount=subscription.amount,
            currency=subscription.currency,
            payment_method="stripe",
            payment_type="SUBSCRIPTION",
            date=datetime.utcnow(),
            status="pending",  # Will be updated after Stripe confirmation
            stripe_payment_intent_id=stripe_subscription.latest_invoice.payment_intent.id,
            data_json={
                "client_secret": stripe_subscription.latest_invoice.payment_intent.client_secret,
                "subscription_id": stripe_subscription.id,
            }
        )
        self.db.add(payment)
        
        # Commit all changes
        self.db.commit()
        self.db.refresh(subscription_user)
        self.db.refresh(payment)

        # Create notification for subscription creation
        self.notification_service.create_notification(
            user_id=subscription_user.user_id,
            title="payment.subscription.created",
            action="PAYMENT",
            data_json={
                "subscription_id": subscription_user.subscription_id,
                "subscription_user_id": subscription_user.id,
                "stripe_subscription_id": subscription_user.stripe_subscription_id,
                "status": subscription_user.status,
                "updated_at": subscription_user.updated_at.isoformat()
            }
        )

        return {
            "subscription_id": stripe_subscription.id,
            "client_secret": stripe_subscription.latest_invoice.payment_intent.client_secret,
            "subscription_user_id": subscription_user.id
        }

    def cancel_stripe_subscription(self, stripe_subscription_id: str) -> dict:
        """Cancel a Stripe subscription"""
        try:
            return stripe.Subscription.delete(stripe_subscription_id)
        except stripe.error.StripeError as e:
            raise ValueError(f"Failed to cancel Stripe subscription: {str(e)}")

    def cancel_subscription(self, subscription_user_id: int) -> dict:
        """Cancel a subscription and its associated Stripe subscription"""
        subscription_user = self.db.query(SubscriptionUser).filter(
            SubscriptionUser.id == subscription_user_id
        ).first()
        
        if not subscription_user:
            raise ValueError("Subscription user not found")

        # Cancel pending payments
        pending_payments = self.db.query(Payment).filter(
            Payment.subscription_user_id == subscription_user_id,
            Payment.status == "pending"
        ).all()
        
        for payment in pending_payments:
            payment.status = "cancelled"
            payment.updated_at = datetime.utcnow()

        # Cancel Stripe subscription if exists
        if subscription_user.stripe_subscription_id:
            try:
                self.cancel_stripe_subscription(subscription_user.stripe_subscription_id)
            except ValueError as e:
                # Log the error but continue with local cancellation
                print(f"Error canceling Stripe subscription: {str(e)}")

        # Update subscription user status
        subscription_user.status = "cancelled"
        subscription_user.updated_at = datetime.utcnow()
        
        self.db.commit()

        # Create notification for subscription cancellation
        self.notification_service.create_notification(
            user_id=subscription_user.user_id,
            title="payment.subscription.canceled",
            action="PAYMENT",
            data_json={
                "subscription_id": subscription_user.subscription_id,
                "subscription_user_id": subscription_user.id,
                "stripe_subscription_id": subscription_user.stripe_subscription_id,
                "status": subscription_user.status,
                "updated_at": subscription_user.updated_at.isoformat()
            }
        )

        return {"status": "success", "message": "Subscription cancelled successfully"}

    def get_subscription_status(self, stripe_subscription_id: str) -> dict:
        """Get the status of a Stripe subscription"""
        return stripe.Subscription.retrieve(stripe_subscription_id)

    def get_subscriptions(self, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        subscriptions = self.db.query(Subscription).offset(skip).limit(limit).all()
        total = self.db.query(Subscription).count()
        
        return {
            "items": subscriptions,
            "total": total,
            "page": (skip // limit) + 1,
            "per_page": limit
        }

    def get_user_subscriptions(self, user_id: int, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        subscriptions = self.db.query(SubscriptionUser).filter(
            SubscriptionUser.user_id == user_id
        ).offset(skip).limit(limit).all()
        
        total = self.db.query(SubscriptionUser).filter(
            SubscriptionUser.user_id == user_id
        ).count()
        
        return {
            "items": subscriptions,
            "total": total,
            "page": (skip // limit) + 1,
            "per_page": limit
        }

    def create_subscription(
        self,
        name: str,
        description: str,
        price: float,
        currency: str,
        interval: str,
        interval_count: int,
        trial_period_days: int = None
    ) -> Subscription:
        """
        Create a new subscription plan
        """
        try:
            # Create Stripe product
            product = stripe.Product.create(
                name=name,
                description=description
            )

            # Create Stripe price
            price_data = {
                "product": product.id,
                "unit_amount": int(price * 100),  # Convert to cents
                "currency": currency.lower(),
                "recurring": {
                    "interval": interval,
                    "interval_count": interval_count
                }
            }

            if trial_period_days:
                price_data["recurring"]["trial_period_days"] = trial_period_days

            stripe_price = stripe.Price.create(**price_data)

            # Create subscription record
            subscription = Subscription(
                name=name,
                description=description,
                price=price,
                currency=currency,
                interval=interval,
                interval_count=interval_count,
                trial_period_days=trial_period_days,
                stripe_product_id=product.id,
                stripe_price_id=stripe_price.id,
                is_active=True
            )
            
            self.db.add(subscription)
            self.db.commit()
            self.db.refresh(subscription)
            
            return subscription

        except stripe.error.StripeError as e:
            self.db.rollback()
            raise ValueError(f"Stripe error: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error creating subscription: {str(e)}")

    def subscribe_user(
        self,
        user_id: int,
        subscription_id: int,
        stripe_customer_id: str
    ) -> SubscriptionUser:
        """
        Subscribe a user to a subscription plan
        """
        try:
            subscription = self.db.query(Subscription).filter(
                Subscription.id == subscription_id,
                Subscription.is_active == True
            ).first()
            
            if not subscription:
                raise ValueError("Subscription not found or inactive")

            # Create Stripe subscription
            stripe_subscription = stripe.Subscription.create(
                customer=stripe_customer_id,
                items=[{"price": subscription.stripe_price_id}],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"]
            )

            # Create subscription user record
            subscription_user = SubscriptionUser(
                user_id=user_id,
                subscription_id=subscription_id,
                status="pending",
                stripe_subscription_id=stripe_subscription.id,
                data_json={
                    "client_secret": stripe_subscription.latest_invoice.payment_intent.client_secret
                }
            )
            
            self.db.add(subscription_user)
            self.db.commit()
            self.db.refresh(subscription_user)
            
            return subscription_user

        except stripe.error.StripeError as e:
            self.db.rollback()
            raise ValueError(f"Stripe error: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error subscribing user: {str(e)}")

    def get_subscription_by_id(self, subscription_id: int) -> Optional[Subscription]:
        """
        Get subscription by ID
        """
        return self.db.query(Subscription).filter(Subscription.id == subscription_id).first()

    def get_subscription_user_by_id(self, subscription_user_id: int) -> Optional[SubscriptionUser]:
        """
        Get subscription user by ID
        """
        return self.db.query(SubscriptionUser).filter(SubscriptionUser.id == subscription_user_id).first()