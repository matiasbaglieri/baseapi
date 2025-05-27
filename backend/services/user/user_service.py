from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from models.session import Session as SessionModel
from sqlalchemy import and_
from datetime import datetime
from core.jwt import JWTManager
from core.logger import logger

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_current_user(self, access_token: str) -> dict:
        """
        Get current user data from access token.
        
        Args:
            access_token (str): JWT access token
            
        Returns:
            dict: User data
            
        Raises:
            HTTPException: If token is invalid or user not found
        """
        try:
            # Verify the access token
            payload = JWTManager.verify_token(access_token)
            user_id = int(payload["sub"])

            # Find active session
            session = self.db.query(SessionModel).filter(
                and_(
                    SessionModel.user_id == user_id,
                    SessionModel.access_token == access_token,
                    SessionModel.expires_at > datetime.utcnow(),
                    SessionModel.is_active == True
                )
            ).first()

            if not session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired session"
                )

            # Get user data
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Update last activity
            session.last_activity = datetime.utcnow()
            self.db.commit()

            return {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role.value,
                "is_verified": user.is_verified,
                "is_active": user.is_active,
                "profile_picture": user.profile_picture,
                "phone_number": user.phone_number,
                "address": user.address,
                "created_at": user.created_at,
                "last_login": user.last_login
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting current user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching user data"
            ) 