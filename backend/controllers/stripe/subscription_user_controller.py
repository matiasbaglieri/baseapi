from fastapi import APIRouter, HTTPException, Depends, Request, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from core.database import get_db
from models.subscription_user import SubscriptionUser
from models.subscription import Subscription
from models.payment import Payment
from services.user import UserService
from services.stripe.subscription_user_service import SubscriptionUserService
from controllers.base_controller import BaseController
from schemas.subscription import SubscriptionUserCreate, SubscriptionUserResponse

class SubscriptionUserController(BaseController[SubscriptionUser]):
    def __init__(self):
        super().__init__(SubscriptionUser)
        self.router = APIRouter(
            tags=["subscription-users"]
        )
        self.setup_routes()

    def setup_routes(self):
        @self.router.post("/create", response_model=dict)
        async def create_subscription(
            subscription_data: SubscriptionUserCreate,
            authorization: Optional[str] = Header(None),
            db: Session = Depends(get_db)
        ):
            """
            Create a new subscription for the authenticated user
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

                # Initialize subscription user service
                subscription_user_service = SubscriptionUserService(db)
                
                # Create subscription and associated payment
                result = await subscription_user_service.create_user_subscription(
                    user_id=current_user.id,
                    subscription_data=subscription_data
                )
                
                return {
                    "message": "Subscription created successfully",
                    "subscription": result
                }
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An error occurred while creating subscription: {str(e)}"
                )

        @self.router.get("/", response_model=List[SubscriptionUserResponse])
        async def get_all_subscriptions(
            authorization: Optional[str] = Header(None),
            db: Session = Depends(get_db)
        ):
            """
            Get all subscriptions for the authenticated user
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

                # Get all subscriptions for user
                subscriptions = db.query(SubscriptionUser).filter(
                    SubscriptionUser.user_id == current_user.id
                ).all()
                
                return subscriptions
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An error occurred while fetching subscriptions: {str(e)}"
                )


# Create router instance
subscription_user_controller = SubscriptionUserController()
router = subscription_user_controller.router
