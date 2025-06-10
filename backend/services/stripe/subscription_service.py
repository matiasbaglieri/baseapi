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
import logging

# Configure logger
logger = logging.getLogger(__name__)

class StripeSubscriptionService:
    def __init__(self, db: Session):
        self.db = db
        stripe.api_key = settings.STRIPE_API_KEY
        self.notification_service = NotificationService(db)

    def create_subscription(self, name: str, subscription_type: str, currency: str, price: float, features: dict = None) -> Subscription:
        """
        Find existing subscription or create new one with Stripe product and price.
        
        Args:
            name (str): Subscription name
            price (float): Subscription price
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
                Subscription.price == price,
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
            
            price_obj = None
            if prices and prices.data:
                # Find price with matching amount
                for p in prices.data:
                    if p.unit_amount == int(price * 100):
                        price_obj = p
                        break
            else:
                # Create new Stripe price
                price_data = {
                    "product": product.id,
                    "unit_amount": int(price * 100),  # Convert to cents
                    "currency": currency.lower(),
                    "recurring": {
                        "interval": subscription_type
                    }
                }
                price_obj = stripe.Price.create(**price_data)

            # Create subscription record
            subscription = Subscription(
                name=name,
                subscription_type=subscription_type,
                currency=currency,
                price=price,
                stripe_product_id=product.id,
                stripe_price_id=price_obj.id,
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
        """Get subscription by ID with features"""
        subscription = self.db.query(Subscription).filter(Subscription.id == subscription_id).first()
        if subscription:
            # Ensure features are loaded
            if not subscription.features:
                subscription.features = {}
            return subscription
        return None

    def get_all_subscriptions(self) -> List[Dict[str, Any]]:
        """Get all subscriptions with complete details and features"""
        subscriptions = self.db.query(Subscription).all()
        result = []
        
        for subscription in subscriptions:
            # Ensure features are loaded and not None
            features = subscription.features or {}
            
            subscription_data = {
                "id": subscription.id,
                "name": subscription.name,
                "subscription_type": subscription.subscription_type,
                "currency": subscription.currency,
                "price": subscription.price,
                "features": features,
                "is_active": subscription.is_active,
                "stripe_price_id": subscription.stripe_price_id,
                "stripe_product_id": subscription.stripe_product_id,
                "created_at": subscription.created_at,
                "updated_at": subscription.updated_at
            }
            result.append(subscription_data)
            
        return result

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
            price=0.00,
            features={
                "api_calls": 1000,
                "support": "Community",
                "advanced_features": False,
                "dedicated_support": False,
                "custom_domains": 0,
                "team_members": 1,
                "storage": "1GB",
                "priority_support": False,
                "sla": "None",
                "custom_integrations": False,
                "rate_limits": "Basic",
                "analytics": "Basic",
                "backup": "None",
                "uptime": "99%"
            }
        )

        # Create PRO subscription
        pro_subscription = self.create_subscription(
            name="PRO",
            subscription_type="month",
            currency="USD",
            price=25.00,
            features={
                "api_calls": 10000,
                "support": "Priority",
                "advanced_features": True,
                "dedicated_support": False,
                "custom_domains": 2,
                "team_members": 5,
                "storage": "10GB",
                "priority_support": True,
                "sla": "Basic",
                "custom_integrations": True,
                "rate_limits": "Advanced",
                "analytics": "Advanced",
                "backup": "Daily",
                "uptime": "99.9%"
            }
        )

        # Create CORPORATE subscription
        corporate_subscription = self.create_subscription(
            name="CORPORATE",
            subscription_type="month",
            currency="USD",
            price=100.00,
            features={
                "api_calls": "Unlimited",
                "support": "24/7",
                "advanced_features": True,
                "dedicated_support": True,
                "custom_domains": "Unlimited",
                "team_members": "Unlimited",
                "storage": "100GB",
                "priority_support": True,
                "sla": "Enterprise",
                "custom_integrations": True,
                "rate_limits": "Custom",
                "analytics": "Enterprise",
                "backup": "Real-time",
                "uptime": "99.99%"
            }
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
            logger.info(f"Creating subscription for user {user_id} with subscription {subscription_id}")
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.error(f"User {user_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            logger.info(f"Found user: {user.email}")

            subscription = self.db.query(Subscription).filter(Subscription.id == subscription_id).first()
            if not subscription:
                logger.error(f"Subscription {subscription_id} not found")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subscription plan not found"
                )
            logger.info(f"Found subscription: {subscription.name}")

            # Check if subscription is active
            if not subscription.is_active:
                logger.warning(f"Subscription {subscription_id} is not active")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This subscription plan is not active"
                )

            # Check if subscription has required Stripe IDs
            if not subscription.stripe_price_id or not subscription.stripe_product_id:
                logger.error(f"Subscription {subscription_id} missing Stripe IDs. Price ID: {subscription.stripe_price_id}, Product ID: {subscription.stripe_product_id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Subscription plan is not properly configured with Stripe"
                )

            # Find existing active subscriptions
            existing_subscriptions = self.db.query(SubscriptionUser).filter(
                SubscriptionUser.user_id == user_id,
                SubscriptionUser.status == "active"
            ).all()
            logger.info(f"Found {len(existing_subscriptions)} existing active subscriptions")

            # Cancel existing subscriptions
            for sub in existing_subscriptions:
                logger.info(f"Cancelling existing subscription {sub.id}")
                sub.status = "cancelled"
                sub.end_date = datetime.utcnow()
                if sub.stripe_subscription_id:
                    try:
                        stripe.Subscription.delete(sub.stripe_subscription_id)
                    except stripe.error.StripeError:
                        logger.warning(f"Failed to delete Stripe subscription {sub.stripe_subscription_id}")

            # Find and cancel pending payments
            pending_payments = self.db.query(Payment).filter(
                Payment.user_id == user_id,
                Payment.status == "pending"
            ).all()
            logger.info(f"Found {len(pending_payments)} pending payments")

            for payment in pending_payments:
                logger.info(f"Cancelling pending payment {payment.id}")
                payment.status = "cancelled"
                payment.updated_at = datetime.utcnow()

            # Get or create Stripe customer
            try:
                logger.info(f"Looking for existing Stripe customer with email {user.email}")
                # First try to find existing customer
                customers = stripe.Customer.list(
                    email=user.email,
                    limit=1
                )
                
                if customers and customers.data:
                    customer = customers.data[0]
                    logger.info(f"Found existing Stripe customer: {customer.id}")
                else:
                    logger.info("No existing customer found, creating new one")
                    # Create new customer if not found
                    customer = stripe.Customer.create(
                        email=user.email,
                        name=f"{user.first_name} {user.last_name}",
                        metadata={
                            "user_id": user.id
                        }
                    )
                    logger.info(f"Created new Stripe customer: {customer.id}")
            except stripe.error.StripeError as e:
                logger.error(f"Error with Stripe customer: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error creating/finding Stripe customer: {str(e)}"
                )

            # Create Stripe checkout session
            try:
                logger.info(f"Creating checkout session for customer {customer.id} with price {subscription.stripe_price_id}")
                session = stripe.checkout.Session.create(
                    customer=customer.id,
                    payment_method_types=['card'],
                    line_items=[{
                        'price': subscription.stripe_price_id,
                        'quantity': 1,
                    }],
                    mode='subscription',
                    success_url=f"{settings.FRONTEND_URL}/subscription/success",
                    cancel_url=f"{settings.FRONTEND_URL}/subscription/cancel",
                    metadata={
                        "user_id": user.id,
                        "subscription_id": subscription.id
                    }
                )
                logger.info(f"Created checkout session: {session.id}")
            except stripe.error.StripeError as e:
                logger.error(f"Error creating checkout session: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error creating checkout session: {str(e)}"
                )

            # Create new subscription user record
            logger.info("Creating subscription user record")
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
            logger.info(f"Created subscription user record: {new_subscription.id}")

            # Create payment record
            logger.info("Creating payment record")
            payment = Payment(
                user_id=user_id,
                subscription_id=subscription_id,
                subscription_user_id=new_subscription.id,
                amount=subscription.price,
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
            logger.info(f"Created payment record: {payment.id}")

            return {
                "checkout_url": session.url,
                "session_id": session.id,
                "subscription_user_id": new_subscription.id,
                "payment_id": payment.id
            }

        except HTTPException:
            logger.error("HTTP Exception occurred")
            self.db.rollback()
            raise
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error occurred: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stripe error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error occurred: {str(e)}")
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
                logger.warning(f"Error canceling Stripe subscription: {str(e)}")

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

   