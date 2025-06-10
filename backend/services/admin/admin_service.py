from sqlalchemy.orm import Session
from typing import Dict, Any, List
from fastapi import HTTPException, status
from models.user import User
from core.roles import UserRole
from core.logger import logger
from schemas.user import UserResponse
from services.user.user_service import UserService

class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def get_current_user(self, access_token: str):
        """Get current user using UserService"""
        return self.user_service.get_current_user(access_token)

    def get_users(self, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        """
        Get paginated list of users.
        
        Args:
            skip (int): Number of records to skip
            limit (int): Maximum number of records to return
            
        Returns:
            Dict[str, Any]: Dictionary containing total count and list of users
        """
        try:
            # Get total count
            total = self.db.query(User).count()
            
            # Get paginated users
            users = self.db.query(User).offset(skip).limit(limit).all()
            
            # Convert to response models
            user_responses = [UserResponse.from_orm(user) for user in users]
            
            return {
                "total": total,
                "items": user_responses,
                "skip": skip,
                "limit": limit
            }
            
        except Exception as e:
            logger.error(f"Error getting users: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching users"
            ) 