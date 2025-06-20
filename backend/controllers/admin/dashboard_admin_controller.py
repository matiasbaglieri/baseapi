from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Dict, Any
from core.database import get_db
from services.admin.admin_service import AdminService
from core.roles import UserRole
from core.logger import logger

router = APIRouter()

@router.get("/stats", response_model=Dict[str, Any])
async def get_stats(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get dashboard statistics including user counts, subscription counts, and payment counts.
    Only accessible by admin users.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    access_token = authorization.split(" ")[1]
    admin_service = AdminService(db)
    
    # Get current user and verify admin role
    current_user = admin_service.get_current_user(access_token)
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can access this endpoint"
        )
    
    return admin_service.get_dashboard_stats() 