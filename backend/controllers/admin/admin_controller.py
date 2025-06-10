from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from core.database import get_db
from services.admin.admin_service import AdminService
from core.roles import UserRole
from schemas.user import UserResponse
from core.logger import logger

router = APIRouter()

@router.get("/users", response_model=Dict[str, Any])
async def get_users(
    skip: int = 0,
    limit: int = 10,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get paginated list of users. Only accessible by admin users.
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
    
    return admin_service.get_users(skip=skip, limit=limit)

@router.get("/subscription-users", response_model=Dict[str, Any])
async def get_subscription_users(
    skip: int = 0,
    limit: int = 10,
    subscription_name: Optional[str] = None,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get paginated list of subscription users with filtering options.
    Only accessible by admin users.
    
    Args:
        skip (int): Number of records to skip
        limit (int): Maximum number of records to return
        subscription_name (str, optional): Filter by subscription name
        status (str, optional): Filter by subscription status
        user_email (str, optional): Filter by user email
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
    
    return admin_service.get_subscription_users(
        skip=skip,
        limit=limit,
        subscription_name=subscription_name,
        status=status,
        user_email=user_email
    )

@router.get("/payments", response_model=Dict[str, Any])
async def get_payments(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    payment_type: Optional[str] = None,
    user_email: Optional[str] = None,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get paginated list of payments with filtering options.
    Only accessible by admin users.
    
    Args:
        skip (int): Number of records to skip
        limit (int): Maximum number of records to return
        status (str, optional): Filter by payment status
        payment_type (str, optional): Filter by payment type
        user_email (str, optional): Filter by user email
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
    
    return admin_service.get_payments(
        skip=skip,
        limit=limit,
        status=status,
        payment_type=payment_type,
        user_email=user_email
    ) 