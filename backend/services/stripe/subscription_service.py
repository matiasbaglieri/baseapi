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
from models.user import User

class StripeSubscriptionService:
    def __init__(self, db: Session):
        self.db = db
        stripe.api_key = settings.STRIPE_API_KEY
        self.notification_service = NotificationService(db)

    def create_subscription(self, name: str, subscription_type: str, currency: str, amount: float, features: dict = None) -> Subscription:
        """
        Find existing subscription or create new one with Stripe product and price.
        
        Args:
            name (str): Subscription name
            amount (float): Subscription amount
            currency (str): Currency code
            subscription_type (str): Subscription interval (month/year)
            features (dict): Subscription features
            
        Returns:
            Subscription: Created or found subscription
        """
        try:
            # Check if subscription already exists
            existing_subscription = self.db.query(Subscription).filter(
                Subscription.name == name,
                Subscription.amount == amount,
                Subscription.currency == currency,
                Subscription.subscription_type == subscription_type
            ).first()

            if existing_subscription:
                return existing_subscription

            # Search for existing Stripe product
            products = stripe.Product.search(
                query=f"name:'{name}'",
                limit=1
            )
            
            product = None
            if products and products.data:
                product = products.data[0]
            else:
                # Create new Stripe product
                product = stripe.Product.create(
                    name=name,
                    description=f"{name} subscription plan"
                )

            # Search for existing price
            prices = stripe.Price.list(
                product=product.id,
                active=True,
                currency=currency.lower(),
                limit=1
            )
            
            price = None
            if prices and prices.data:
                # Find price with matching amount
                for p in prices.data:
                    if p.unit_amount == int(amount * 100):
                        price = p
                        break
            else:
                # Create new Stripe price
                price_data = {
                    "product": product.id,
                    "unit_amount": int(amount * 100),  # Convert to cents
                    "currency": currency.lower(),
                    "recurring": {
                        "interval": subscription_type
                    }
                }
                price = stripe.Price.create(**price_data)

            # Create subscription record
            subscription = Subscription(
                name=name,
                subscription_type=subscription_type,
                currency=currency,
                amount=amount,
                stripe_product_id=product.id,
                stripe_price_id=price.id,
                features=features
            )
            
            self.db.add(subscription)
            self.db.commit()
            self.db.refresh(subscription)
            
            return subscription

        except stripe.error.StripeError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stripe error: {str(e)}"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating subscription: {str(e)}"
            )

    def get_subscription(self, subscription_id: int) -> Optional[Subscription]:
        return self.db.query(Subscription).filter(Subscription.id == subscription_id).first()

    def get_all_subscriptions(self) -> List[Subscription]:
        return self.db.query(Subscription).all()

    def init_subscriptions(self) -> List[Subscription]:
        """Initialize default subscriptions if they don't exist"""
        existing_subscriptions = self.get_all_subscriptions()
        if existing_subscriptions:
            return existing_subscriptions

        # Create FREE subscription
        free_subscription = self.create_subscription(
            name="FREE",
            subscription_type="month",
            currency="USD",
            amount=0.00,
            features={"api_calls": 1000, "support": "Community"}
        )

        # Create PRO subscription
        pro_subscription = self.create_subscription(
            name="PRO",
            subscription_type="month",
            currency="USD",
            amount=25.00,
            features={"api_calls": 10000, "support": "Priority", "advanced_features": True}
        )

        # Create CORPORATE subscription
        corporate_subscription = self.create_subscription(
            name="CORPORATE",
            subscription_type="month",
            currency="USD",
            amount=100.00,
            features={"api_calls": "Unlimited", "support": "24/7", "advanced_features": True, "dedicated_support": True}
        )

        return [free_subscription, pro_subscription, corporate_subscription]

    def create_customer_subscription(self, user_id: int, subscription_id: int) -> dict:
        """
        Create a subscription for a customer.
        
        Args:
            user_id (int): ID of the user
            subscription_id (int): ID of the subscription plan
            
        Returns:
            dict: Subscription details with checkout URL
        """
        try:
            # Get user and subscription
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            subscription = self.db.query(Subscription).filter(Subscription.id == subscription_id).first()
            if not subscription:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subscription plan not found"
                )

            # Find existing active subscriptions
            existing_subscriptions = self.db.query(SubscriptionUser).filter(
                SubscriptionUser.user_id == user_id,
                SubscriptionUser.status == "active"
            ).all()

            # Cancel existing subscriptions
            for sub in existing_subscriptions:
                sub.status = "cancelled"
                sub.end_date = datetime.utcnow()
                if sub.stripe_subscription_id:
                    try:
                        stripe.Subscription.delete(sub.stripe_subscription_id)
                    except stripe.error.StripeError:
                        pass  # Ignore if subscription already cancelled

            # Find and cancel pending payments
            pending_payments = self.db.query(Payment).filter(
                Payment.user_id == user_id,
                Payment.status == "pending"
            ).all()

            for payment in pending_payments:
                payment.status = "cancelled"
                if payment.stripe_payment_intent_id:
                    try:
                        stripe.PaymentIntent.cancel(payment.stripe_payment_intent_id)
                    except stripe.error.StripeError:
                        pass  # Ignore if payment already cancelled
                payment.updated_at = datetime.utcnow()
            # Get or create Stripe customer
            customer = stripe.Customer.create(
                email=user.email,
                name=f"{user.first_name} {user.last_name}",
                metadata={
                    "user_id": user.id
                }
            )

            # Create Stripe checkout session
            session = stripe.checkout.Session.create(
                customer=customer.id,
                payment_method_types=['card'],
                line_items=[{
                    'price': subscription.stripe_price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{settings.FRONTEND_URL}/subscription/success?session_id={session.id}",
                cancel_url=f"{settings.FRONTEND_URL}/subscription/cancel?session_id={session.id}",
                metadata={
                    "user_id": user.id,
                    "subscription_id": subscription.id
                }
            )

            # Create new subscription user record
            new_subscription = SubscriptionUser(
                user_id=user_id,
                subscription_id=subscription_id,
                status="pending",
                start_date=datetime.utcnow(),
                stripe_customer_id=customer.id,
                data_json={
                    "checkout_session_id": session.id
                }
            )
            
            self.db.add(new_subscription)
            self.db.flush()  # Get the ID without committing

            # Create payment record
            payment = Payment(
                user_id=user_id,
                subscription_id=subscription_id,
                subscription_user_id=new_subscription.id,
                amount=subscription.amount,
                currency=subscription.currency,
                payment_method="stripe",
                payment_type="SUBSCRIPTION",
                date=datetime.utcnow(),
                status="pending",
                stripe_payment_intent_id=session.payment_intent,
                data_json={
                    "checkout_session_id": session.id,
                    "customer_id": customer.id
                }
            )
            
            self.db.add(payment)
            self.db.commit()
            self.db.refresh(new_subscription)

            return {
                "checkout_url": session.url,
                "session_id": session.id,
                "subscription_user_id": new_subscription.id,
                "payment_id": payment.id
            }

        except stripe.error.StripeError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stripe error: {str(e)}"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating subscription: {str(e)}"
            )

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

   