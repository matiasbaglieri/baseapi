from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Dict, Any
import os
from dotenv import load_dotenv
from core.database import get_db
from services.user.user_service import UserService
from core.roles import UserRole
from schemas.user import UserResponse, ChangeRoleRequest

load_dotenv()

router = APIRouter()

@router.post("/upgrade-to-admin", response_model=UserResponse)
async def upgrade_to_admin(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Upgrade a user to admin role. Only accessible by users with USER_ADMIN role.
    """
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    access_token = authorization.split(" ")[1]
    user_service = UserService(db)
    
    # First get the current user to ensure authentication
    current_user = user_service.get_current_user(access_token)
    # Check if current user has USER_ADMIN role
    if current_user.email != os.getenv("USER_ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    
    user_service = UserService(db)
    updated_user = user_service.update_user_role(current_user.id, UserRole.ADMIN.value)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user 

@router.post("/change-role", response_model=UserResponse)
async def change_role(
    request: ChangeRoleRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Change a user's role. Only accessible by admin users.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    access_token = authorization.split(" ")[1]
    user_service = UserService(db)
    
    # Get current user and verify admin role
    current_user = user_service.get_current_user(access_token)
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can change roles"
        )
    
    # Validate new role exists in UserRole
    try:
        role = UserRole(request.new_role)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {[r.value for r in UserRole]}"
        )
    
    # Find user by email
    target_user = user_service.get_user_by_email(request.email)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user role
    updated_user = user_service.update_user_role(target_user.id, role.value)
    return updated_user 
