from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from services.stripe.subscription_service import StripeSubscriptionService
from models.subscription import Subscription
from schemas.subscription import SubscriptionCreate, SubscriptionResponse
from core.config import settings

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
    stripe_customer_id: str,
    subscription_service: StripeSubscriptionService = Depends(get_subscription_service)
):
    """
    Create a subscription for a customer
    """
    try:
        result = subscription_service.create_customer_subscription(
            subscription_id=subscription_id,
            stripe_customer_id=stripe_customer_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{stripe_subscription_id}/cancel")
def cancel_subscription(
    stripe_subscription_id: str,
    subscription_service: StripeSubscriptionService = Depends(get_subscription_service)
):
    """
    Cancel a subscription
    """
    try:
        result = subscription_service.cancel_subscription(stripe_subscription_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 