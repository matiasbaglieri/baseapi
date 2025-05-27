from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from models.session import Session as SessionModel
from core.jwt import JWTManager
from core.roles import UserRole
from core.logger import logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get refresh token expiration days from environment
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

class RefreshTokenService:
    def __init__(self, db: Session):
        self.db = db

    def refresh_token(self, refresh_token: str, ip_address: str, user_agent: str):
        """
        Refresh the access token using a refresh token.
        Creates a new session if the current one is expired.
        
        Args:
            refresh_token (str): The refresh token to use
            ip_address (str): Client's IP address
            user_agent (str): Client's user agent
            
        Returns:
            dict: Response containing new tokens and status
            
        Raises:
            HTTPException: If token refresh fails
        """
        try:
            # Verify the refresh token
            payload = JWTManager.verify_token(refresh_token)
            user_id = int(payload["sub"])
            email = payload["email"]
            try:
                role = UserRole(payload["role"])  # Convert string to UserRole enum
            except ValueError as e:
                logger.warning(f"Could not parse role '{payload.get('role')}', using default value: {str(e)}")
                role = UserRole.USER  # Default to USER role if parsing fails

            # Check for existing valid session
            existing_session = self.db.query(SessionModel).filter(
                and_(
                    SessionModel.user_id == user_id,
                    SessionModel.refresh_token == refresh_token,
                    SessionModel.expires_at > datetime.utcnow(),
                    SessionModel.is_active == True
                )
            ).first()

            if existing_session:
                # Update existing session with new tokens
                tokens = JWTManager.create_tokens_response(
                    user_id=user_id,
                    email=email,
                    role=role
                )
                
                existing_session.access_token = tokens["access_token"]
                existing_session.refresh_token = tokens["refresh_token"]
                existing_session.last_activity = datetime.utcnow()
                existing_session.ip_address = ip_address
                existing_session.user_agent = user_agent
                
                access_token = tokens["access_token"]
                refresh_token = tokens["refresh_token"]
            else:
                # Create new session with new tokens
                tokens = JWTManager.create_tokens_response(
                    user_id=user_id,
                    email=email,
                    role=role
                )
                
                new_session = SessionModel(
                    user_id=user_id,
                    access_token=tokens["access_token"],
                    refresh_token=tokens["refresh_token"],
                    token_type="bearer",
                    ip_address=ip_address,
                    user_agent=user_agent,
                    expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
                )
                
                self.db.add(new_session)
                access_token = tokens["access_token"]
                refresh_token = tokens["refresh_token"]

            self.db.commit()

            return {
                "message": "Token refreshed successfully",
                "status": "success",
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                    "expires_in": 900  # 15 minutes in seconds
                }
            }

        except Exception as e:
            logger.error(f"Token refresh failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            ) 