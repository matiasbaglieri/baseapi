from enum import Enum
from typing import List

class UserRole(str, Enum):
    """
    Enum defining user roles in the system.
    """
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"
    
    @classmethod
    def get_hierarchy(cls, role: str) -> List[str]:
        """
        Get the hierarchy of roles for a given role.
        Higher roles have access to lower role permissions.
        
        Args:
            role: The role to get hierarchy for
            
        Returns:
            List of roles in hierarchy order
        """
        if role == cls.ADMIN:
            return [cls.ADMIN, cls.MODERATOR, cls.USER, cls.GUEST]
        elif role == cls.MODERATOR:
            return [cls.MODERATOR, cls.USER, cls.GUEST]
        elif role == cls.USER:
            return [cls.USER, cls.GUEST]
        elif role == cls.GUEST:
            return [cls.GUEST]
        return [] 