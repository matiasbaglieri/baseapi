from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Any
import jwt
from fastapi import HTTPException, status
from .config import settings
from .roles import UserRole

class JWTManager:
    """
    JWT token management class that handles token creation, verification, and refresh.
    Implements best practices for JWT token handling using PyJWT.
    """
    
    @staticmethod
    def create_token_pair(user_id: int, email: str, role: UserRole = UserRole.USER) -> Tuple[str, str]:
        """
        Create a pair of access and refresh tokens for a user.
        
        Args:
            user_id: The user's ID
            email: The user's email
            role: The user's role (defaults to USER)
            
        Returns:
            Tuple containing (access_token, refresh_token)
        """
        print("create_token_pair", user_id, email, role)
        # Create access token
        access_token = JWTManager.create_access_token(user_id, email, role)
        
        # Create refresh token
        refresh_token = JWTManager.create_refresh_token(user_id, email, role)
        print("access_token", access_token)
        print("refresh_token", refresh_token)
        return access_token, refresh_token
    
    @staticmethod
    def create_access_token(user_id: int, email: str, role: UserRole = UserRole.USER) -> str:
        """
        Create an access token for a user.
        
        Args:
            user_id: The user's ID
            email: The user's email
            role: The user's role (defaults to USER)
            
        Returns:
            JWT access token string
        """
        expires_delta = settings.JWT_ACCESS_TOKEN_EXPIRE
        return JWTManager._create_token(
            user_id=user_id,
            email=email,
            role=role,
            token_type=settings.JWT_TOKEN_TYPE_ACCESS,
            expires_delta=expires_delta
        )
    
    @staticmethod
    def create_refresh_token(user_id: int, email: str, role: UserRole = UserRole.USER) -> str:
        """
        Create a refresh token for a user.
        
        Args:
            user_id: The user's ID
            email: The user's email
            role: The user's role (defaults to USER)
            
        Returns:
            JWT refresh token string
        """
        expires_delta = settings.JWT_REFRESH_TOKEN_EXPIRE
        return JWTManager._create_token(
            user_id=user_id,
            email=email,
            role=role,
            token_type=settings.JWT_TOKEN_TYPE_REFRESH,
            expires_delta=expires_delta
        )
    
    @staticmethod
    def _create_token(
        user_id: int,
        email: str,
        role: UserRole,
        token_type: str,
        expires_delta: timedelta
    ) -> str:
        """
        Create a JWT token with the specified parameters.
        
        Args:
            user_id: The user's ID
            email: The user's email
            role: The user's role
            token_type: Type of token (access/refresh)
            expires_delta: Token expiration time
            
        Returns:
            JWT token string
        """
        print("create_token", user_id, email, role, token_type, expires_delta)
        now = datetime.utcnow()
        expire = now + expires_delta
        
        # Standard JWT claims
        to_encode = {
            "sub": str(user_id),  # Subject (user ID)
            "email": email,
            "role": role.value,
            "type": token_type,
            "exp": expire,  # Expiration time
            "iat": now,     # Issued at
            "nbf": now,     # Not before
            "jti": f"{user_id}-{now.timestamp()}",  # JWT ID (unique token identifier)
            "iss": settings.JWT_ISSUER,  # Issuer
            "aud": settings.JWT_AUDIENCE  # Audience
        }
        
        # Create token with headers
        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
            headers={
                "typ": "JWT",
                "alg": settings.JWT_ALGORITHM
            }
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
                algorithms=[settings.JWT_ALGORITHM],
                issuer=settings.JWT_ISSUER,
                audience=settings.JWT_AUDIENCE,
                leeway=settings.JWT_LEEWAY,
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iat": True,
                    "verify_nbf": True,
                    "require": ["exp", "iat", "nbf", "sub", "type", "iss", "aud", "jti"]
                }
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.InvalidTokenError("Token has expired")
        except jwt.InvalidIssuerError:
            raise jwt.InvalidTokenError("Invalid token issuer")
        except jwt.InvalidAudienceError:
            raise jwt.InvalidTokenError("Invalid token audience")
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
            role = UserRole(payload["role"])
            
            # Create new token pair
            return JWTManager.create_token_pair(user_id, email, role)
            
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
            role = UserRole(payload["role"])
            
            # Create new access token
            return JWTManager.create_access_token(user_id, email, role)
            
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f"Invalid refresh token: {str(e)}")

    @staticmethod
    def create_tokens_response(user_id: int, email: str, role: UserRole = UserRole.USER) -> Dict[str, str]:
        """
        Create new access and refresh tokens for a user and return them in a response format.
        
        Args:
            user_id: The user's ID
            email: The user's email
            role: The user's role (defaults to USER)
            
        Returns:
            Dict containing access_token and refresh_token
        """
        print("create_tokens_response", user_id)
        
        access_token, refresh_token = JWTManager.create_token_pair(user_id, email, role)
        print("access_token", access_token)
        print("refresh_token", refresh_token)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": int(settings.JWT_ACCESS_TOKEN_EXPIRE.total_seconds())
        }

    @staticmethod
    def refresh_tokens_response(refresh_token: str) -> Dict[str, str]:
        """
        Refresh the access and refresh tokens and return them in a response format.
        
        Args:
            refresh_token: The current refresh token
            
        Returns:
            Dict containing new access_token and refresh_token
            
        Raises:
            HTTPException: If refresh token is invalid
        """
        try:
            new_access_token, new_refresh_token = JWTManager.rotate_refresh_token(refresh_token)
            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer",
                "expires_in": int(settings.JWT_ACCESS_TOKEN_EXPIRE.total_seconds())
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            ) 