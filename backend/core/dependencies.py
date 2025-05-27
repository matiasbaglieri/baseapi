from typing import Optional, List, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_utils import JWTManager
from .roles import UserRole

# Create security scheme
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    FastAPI dependency to get the current user from the JWT token.
    Validates the access token and returns the user information.
    
    Args:
        credentials: The HTTP authorization credentials containing the token
        
    Returns:
        dict: The user information from the token
        
    Raises:
        HTTPException: If the token is invalid or expired
    """
    try:
        # Verify the token
        payload = JWTManager.verify_token(credentials.credentials)
        
        # Ensure it's an access token
        if not JWTManager.is_access_token(credentials.credentials):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type. Access token required."
            )
        
        return {
            "user_id": int(payload["sub"]),
            "email": payload["email"],
            "role": payload.get("role", UserRole.USER)  # Default to USER role if not specified
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

async def get_current_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    FastAPI dependency to get the current refresh token.
    Validates the refresh token and returns the token information.
    
    Args:
        credentials: The HTTP authorization credentials containing the token
        
    Returns:
        dict: The token information
        
    Raises:
        HTTPException: If the token is invalid or expired
    """
    try:
        # Verify the token
        payload = JWTManager.verify_token(credentials.credentials)
        
        # Ensure it's a refresh token
        if not JWTManager.is_refresh_token(credentials.credentials):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type. Refresh token required."
            )
        
        return {
            "user_id": int(payload["sub"]),
            "email": payload["email"],
            "role": payload.get("role", UserRole.USER),  # Default to USER role if not specified
            "token": credentials.credentials
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

async def get_optional_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[dict]:
    """
    FastAPI dependency to get the current user if a valid token is provided.
    Returns None if no token is provided or if the token is invalid.
    
    Args:
        credentials: The HTTP authorization credentials containing the token
        
    Returns:
        Optional[dict]: The user information if a valid token is provided, None otherwise
    """
    if not credentials:
        return None
        
    try:
        # Verify the token
        payload = JWTManager.verify_token(credentials.credentials)
        
        # Ensure it's an access token
        if not JWTManager.is_access_token(credentials.credentials):
            return None
        
        return {
            "user_id": int(payload["sub"]),
            "email": payload["email"],
            "role": payload.get("role", UserRole.USER)  # Default to USER role if not specified
        }
    except Exception:
        return None

def require_roles(allowed_roles: Union[UserRole, List[UserRole]]) -> callable:
    """
    Dependency factory for role-based access control.
    Creates a dependency that checks if the current user has the required role(s).
    
    Args:
        allowed_roles: Single role or list of roles that are allowed to access the endpoint
        
    Returns:
        Dependency function that checks user roles
    """
    if isinstance(allowed_roles, UserRole):
        allowed_roles = [allowed_roles]
    
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        """
        Check if the current user has the required role.
        
        Args:
            current_user: The current user information from get_current_user dependency
            
        Returns:
            dict: The current user information if authorized
            
        Raises:
            HTTPException: If the user is not authorized
        """
        user_role = current_user.get("role", UserRole.USER)
        
        # Get all roles the user has access to based on hierarchy
        user_roles = UserRole.get_hierarchy(user_role)
        
        # Check if any of the allowed roles are in the user's role hierarchy
        if not any(role in user_roles for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. Required roles: {[role.value for role in allowed_roles]}"
            )
        
        return current_user
    
    return role_checker 