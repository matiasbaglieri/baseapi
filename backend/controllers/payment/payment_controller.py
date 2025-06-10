from fastapi import APIRouter, HTTPException, Depends, Query, status, Header
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from core.database import get_db
from models.payment import Payment
from services.payment.payment_service import PaymentService
from services.user import UserService
from controllers.base_controller import BaseController
from schemas.payment import PaymentTransactionCreate, PaymentResponse
from typing import List

class PaymentController(BaseController[Payment]):
    def __init__(self):
        super().__init__(Payment)
        self.router = APIRouter(tags=["payments"])
        self.setup_routes()

    def setup_routes(self):
        @self.router.get("/user", response_model=Dict[str, Any])
        async def get_user_payments(
            page: int = Query(1, ge=1, description="Page number"),
            per_page: int = Query(10, ge=1, le=100, description="Items per page"),
            authorization: Optional[str] = Header(None),
            db: Session = Depends(get_db)
        ):
            """
            Get paginated list of user's payments with related subscription data
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

                # Initialize payment service
                payment_service = PaymentService(db)
                
                # Calculate skip for pagination
                skip = (page - 1) * per_page
                
                # Get payments with pagination
                result = payment_service.get_user_payments(
                    user_id=current_user.id,
                    skip=skip,
                    limit=per_page
                )
                
                return result
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An error occurred while retrieving payments: {str(e)}"
                )

        @self.router.post("/transaction", response_model=dict)
        async def create_payment_transaction(
            payment_data: PaymentTransactionCreate,
            authorization: Optional[str] = Header(None),
            db: Session = Depends(get_db)
        ):
            """
            Create a new payment transaction
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

                # Initialize payment service
                payment_service = PaymentService(db)
                
                # Create payment transaction
                result = payment_service.find_or_create_payment_transaction(
                    user_id=current_user.id,
                    amount=payment_data.amount,
                    currency=payment_data.currency,
                    description=payment_data.description
                )
                
                return result
                
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An error occurred while creating payment: {str(e)}"
                )

# Create router instance
payment_controller = PaymentController()
router = payment_controller.router
