from fastapi import APIRouter, Depends, HTTPException, Query, status, Header
from sqlalchemy.orm import Session
from typing import Optional, List
from core.database import get_db
from models.notification import Notification
from schemas.notification import NotificationCreate, NotificationUpdate, NotificationResponse
from services.notification.notification_service import NotificationService
from services.user import UserService
from controllers.base_controller import BaseController

class NotificationController(BaseController[Notification]):
    def __init__(self):
        super().__init__(Notification)
        self.router = APIRouter(tags=["notifications"])
        self.setup_routes()

    def setup_routes(self):
        @self.router.get("/", response_model=List[NotificationResponse])
        async def get_user_notifications(
            page: int = Query(1, ge=1, description="Page number"),
            per_page: int = Query(10, ge=1, le=100, description="Items per page"),
            authorization: Optional[str] = Header(None),
            db: Session = Depends(get_db)
        ):
            """
            Get paginated list of user's notifications
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

                # Initialize notification service
                notification_service = NotificationService(db)
                
                # Calculate skip for pagination
                skip = (page - 1) * per_page
                
                # Get notifications with pagination
                notifications = notification_service.get_user_notifications(
                    user_id=current_user.id,
                    skip=skip,
                    limit=per_page
                )
                
                return notifications
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An error occurred while retrieving notifications: {str(e)}"
                )

# Create router instance
notification_controller = NotificationController()
router = notification_controller.router 