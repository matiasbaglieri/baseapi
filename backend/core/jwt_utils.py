from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import jwt
from .config import settings

class JWTManager:
    @staticmethod
    def create_token_pair(user_id: int, email: str) -> Tuple[str, str]:
        """
        Create a pair of access and refresh tokens for a user.
        
        Args:
            user_id: The user's ID
            email: The user's email
            
        Returns:
            Tuple containing (access_token, refresh_token)
        """
        # Create access token
        access_token = JWTManager.create_access_token(user_id, email)
        
        # Create refresh token
        refresh_token = JWTManager.create_refresh_token(user_id, email)
        
        return access_token, refresh_token
    
    @staticmethod
    def create_access_token(user_id: int, email: str) -> str:
        """
        Create an access token for a user.
        
        Args:
            user_id: The user's ID
            email: The user's email
            
        Returns:
            JWT access token string
        """
        expires_delta = settings.JWT_ACCESS_TOKEN_EXPIRE
        return JWTManager._create_token(
            user_id=user_id,
            email=email,
            token_type=settings.JWT_TOKEN_TYPE_ACCESS,
            expires_delta=expires_delta
        )
    
    @staticmethod
    def create_refresh_token(user_id: int, email: str) -> str:
        """
        Create a refresh token for a user.
        
        Args:
            user_id: The user's ID
            email: The user's email
            
        Returns:
            JWT refresh token string
        """
        expires_delta = settings.JWT_REFRESH_TOKEN_EXPIRE
        return JWTManager._create_token(
            user_id=user_id,
            email=email,
            token_type=settings.JWT_TOKEN_TYPE_REFRESH,
            expires_delta=expires_delta
        )
    
    @staticmethod
    def _create_token(
        user_id: int,
        email: str,
        token_type: str,
        expires_delta: timedelta
    ) -> str:
        """
        Create a JWT token with the specified parameters.
        
        Args:
            user_id: The user's ID
            email: The user's email
            token_type: Type of token (access/refresh)
            expires_delta: Token expiration time
            
        Returns:
            JWT token string
        """
        expire = datetime.utcnow() + expires_delta
        
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "type": token_type,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
    
    @staticmethod
    def verify_token(token: str) -> Dict:
        """
        Verify and decode a JWT token.
        
        Args:
            token: The JWT token to verify
            
        Returns:
            Decoded token payload
            
        Raises:
            jwt.InvalidTokenError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.InvalidTokenError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f"Invalid token: {str(e)}")
    
    @staticmethod
    def get_token_type(token: str) -> Optional[str]:
        """
        Get the type of a JWT token (access/refresh).
        
        Args:
            token: The JWT token to check
            
        Returns:
            Token type string or None if invalid
        """
        try:
            payload = JWTManager.verify_token(token)
            return payload.get("type")
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def is_access_token(token: str) -> bool:
        """
        Check if a token is an access token.
        
        Args:
            token: The JWT token to check
            
        Returns:
            True if token is an access token, False otherwise
        """
        return JWTManager.get_token_type(token) == settings.JWT_TOKEN_TYPE_ACCESS
    
    @staticmethod
    def is_refresh_token(token: str) -> bool:
        """
        Check if a token is a refresh token.
        
        Args:
            token: The JWT token to check
            
        Returns:
            True if token is a refresh token, False otherwise
        """
        return JWTManager.get_token_type(token) == settings.JWT_TOKEN_TYPE_REFRESH

    @staticmethod
    def rotate_refresh_token(refresh_token: str) -> Tuple[str, str]:
        """
        Rotate a refresh token by creating a new access token and refresh token pair.
        This invalidates the old refresh token.
        
        Args:
            refresh_token: The current refresh token
            
        Returns:
            Tuple containing (new_access_token, new_refresh_token)
            
        Raises:
            jwt.InvalidTokenError: If the refresh token is invalid or expired
        """
        try:
            # Verify the refresh token
            payload = JWTManager.verify_token(refresh_token)
            
            # Ensure it's actually a refresh token
            if not JWTManager.is_refresh_token(refresh_token):
                raise jwt.InvalidTokenError("Token is not a refresh token")
            
            # Extract user information
            user_id = int(payload["sub"])
            email = payload["email"]
            
            # Create new token pair
            return JWTManager.create_token_pair(user_id, email)
            
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f"Invalid refresh token: {str(e)}")
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> str:
        """
        Create a new access token using a refresh token.
        This does not rotate the refresh token.
        
        Args:
            refresh_token: The current refresh token
            
        Returns:
            New access token
            
        Raises:
            jwt.InvalidTokenError: If the refresh token is invalid or expired
        """
        try:
            # Verify the refresh token
            payload = JWTManager.verify_token(refresh_token)
            
            # Ensure it's actually a refresh token
            if not JWTManager.is_refresh_token(refresh_token):
                raise jwt.InvalidTokenError("Token is not a refresh token")
            
            # Extract user information
            user_id = int(payload["sub"])
            email = payload["email"]
            
            # Create new access token
            return JWTManager.create_access_token(user_id, email)
            
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f"Invalid refresh token: {str(e)}") 