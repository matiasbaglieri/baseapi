from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from services.stripe.subscription_service import StripeSubscriptionService
from services.user.user_service import UserService
from models.subscription import Subscription
from models.subscription_user import SubscriptionUser
from models.payment import Payment
from schemas.subscription import SubscriptionCreate, SubscriptionResponse
from core.config import settings
import stripe
from datetime import datetime

router = APIRouter(
    tags=["subscriptions"]
)

def get_subscription_service(db: Session = Depends(get_db)) -> StripeSubscriptionService:
    return StripeSubscriptionService(db)

@router.post("/init", response_model=List[SubscriptionResponse])
def init_subscriptions(
    subscription_service: StripeSubscriptionService = Depends(get_subscription_service)
):
    """
    Initialize default subscriptions (PRO and CORPORATE)
    """
    subscriptions = subscription_service.init_subscriptions()
    return subscriptions

@router.get("/", response_model=List[SubscriptionResponse])
def get_subscriptions(
    subscription_service: StripeSubscriptionService = Depends(get_subscription_service)
):
    """
    Get all available subscriptions
    """
    return subscription_service.get_all_subscriptions()

@router.get("/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(
    subscription_id: int,
    subscription_service: StripeSubscriptionService = Depends(get_subscription_service)
):
    """
    Get a specific subscription by ID
    """
    subscription = subscription_service.get_subscription(subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@router.post("/{subscription_id}/subscribe")
def create_subscription(
    subscription_id: int,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
    subscription_service: StripeSubscriptionService = Depends(get_subscription_service)
):
    """
    Create a subscription for a customer
    """
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header"
            )
        
        access_token = authorization.split(" ")[1]
        user_service = UserService(db)
        
        # First get the current user to ensure authentication
        current_user = user_service.get_current_user(access_token)
        result = subscription_service.create_customer_subscription(
            user_id=current_user.id,
            subscription_id=subscription_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{subscription_user_id}/cancel")
def cancel_subscription(
    subscription_user_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
    subscription_service: StripeSubscriptionService = Depends(get_subscription_service)
):
    """
    Cancel a subscription
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    try:
        # Get current user from token
        access_token = authorization.split(" ")[1]
        user_service = UserService(db)
        current_user = user_service.get_current_user(access_token)

        # Get subscription user
        subscription_user = db.query(SubscriptionUser).filter(
            SubscriptionUser.id == subscription_user_id,
            SubscriptionUser.user_id == current_user.id
        ).first()

        if not subscription_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found"
            )

        # Cancel subscription in Stripe if stripe_subscription_id exists
        if subscription_user.stripe_subscription_id:
            try:
                stripe.Subscription.delete(subscription_user.stripe_subscription_id)
            except stripe.error.StripeError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stripe error: {str(e)}"
                )

        # Update subscription user status
        subscription_user.status = "cancelled"
        subscription_user.updated_at = datetime.utcnow()

        # Find and cancel all payments for this subscription user
        payments = db.query(Payment).filter(
            Payment.subscription_user_id == subscription_user.id
        ).all()

        for payment in payments:
            payment.status = "cancelled"
            payment.updated_at = datetime.utcnow()
            
            # Cancel Stripe payment intent if exists
            if payment.stripe_payment_intent_id:
                try:
                    stripe.PaymentIntent.cancel(payment.stripe_payment_intent_id)
                except stripe.error.StripeError:
                    pass  # Ignore if payment already cancelled

        db.commit()

        return {
            "status": "success",
            "message": "Subscription and all associated payments cancelled",
            "subscription_id": subscription_user.id,
            "cancelled_payments": len(payments)
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error cancelling subscription: {str(e)}"
        )

@router.get("/success")
def subscription_success(
    session_id: str,
    db: Session = Depends(get_db),
    subscription_service: StripeSubscriptionService = Depends(get_subscription_service)
):
    """
    Handle successful subscription payment
    """
    try:
        # Retrieve the checkout session
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Get subscription user from database
        subscription_user = db.query(SubscriptionUser).filter(
            SubscriptionUser.data_json['checkout_session_id'].astext == session_id
        ).first()
        
        if not subscription_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found"
            )

        # Update subscription user status
        subscription_user.status = "active"
        subscription_user.stripe_subscription_id = session.subscription
        subscription_user.updated_at = datetime.utcnow()

        # Update payment status
        payment = db.query(Payment).filter(
            Payment.subscription_user_id == subscription_user.id,
            Payment.status == "pending"
        ).first()

        if payment:
            payment.status = "completed"
            payment.updated_at = datetime.utcnow()
            payment.data_json = {
                **payment.data_json,
                "subscription_id": session.subscription,
                "payment_intent": session.payment_intent
            }

        db.commit()

        return {
            "status": "success",
            "message": "Subscription activated successfully",
            "subscription_id": subscription_user.id
        }

    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing subscription: {str(e)}"
        )

@router.get("/cancel")
def subscription_cancel(
    session_id: str,
    db: Session = Depends(get_db),
    subscription_service: StripeSubscriptionService = Depends(get_subscription_service)
):
    """
    Handle cancelled subscription payment
    """
    try:
        # Get subscription user from database
        subscription_user = db.query(SubscriptionUser).filter(
            SubscriptionUser.data_json['checkout_session_id'].astext == session_id
        ).first()
        
        if not subscription_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found"
            )

        # Update subscription user status
        subscription_user.status = "cancelled"
        subscription_user.updated_at = datetime.utcnow()

        # Find and cancel all payments for this subscription user
        payments = db.query(Payment).filter(
            Payment.subscription_user_id == subscription_user.id
        ).all()

        for payment in payments:
            payment.status = "cancelled"
            payment.updated_at = datetime.utcnow()
            
            # Cancel Stripe payment intent if exists
            if payment.stripe_payment_intent_id:
                try:
                    stripe.PaymentIntent.cancel(payment.stripe_payment_intent_id)
                except stripe.error.StripeError:
                    pass  # Ignore if payment already cancelled

        db.commit()

        return {
            "status": "cancelled",
            "message": "Subscription and all associated payments cancelled",
            "subscription_id": subscription_user.id,
            "cancelled_payments": len(payments)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error cancelling subscription: {str(e)}"
        ) 