"""
access.py - Access control and authorization for RK-OS security system
"""

import time
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class AccessControlManager:
    """
    Advanced access control manager with role-based permissions
    """
    
    def __init__(self):
        """Initialize access control system"""
        self.permissions = {}
        self.roles = {}
        self.role_permissions = {}
        
        logger.info("Access Control Manager initialized")
        
    def create_role(self, role_name: str, permissions: list) -> bool:
        """
        Create a new user role with associated permissions
        
        Args:
            role_name (str): Name of the role
            permissions (list): List of permission names
            
        Returns:
            bool: True if successful
        """
        try:
            self.roles[role_name] = {
                'permissions': set(permissions),
                'created_at': time.time()
            }
            
            # Store role permissions for quick lookup
            self.role_permissions[role_name] = set(permissions)
            
            logger.info(f"Role '{role_name}' created with {len(permissions)} permissions")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create role '{role_name}': {str(e)}")
            return False
    
    def assign_role_to_user(self, user: str, role: str) -> bool:
        """
        Assign a role to a specific user
        
        Args:
            user (str): User identifier
            role (str): Role name to assign
            
        Returns:
            bool: True if successful
        """
        try:
            # Check if role exists
            if role not in self.roles:
                raise ValueError(f"Role '{role}' does not exist")
            
            # Assign role to user  
            if 'roles' not in self.permissions:
                self.permissions['roles'] = {}
                
            self.permissions['roles'][user] = role
            
            logger.info(f"Assigned role '{role}' to user '{user}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to assign role '{role}' to user '{user}': {str(e)}")
            return False
    
    def grant_permission(self, user: str, permission: str) -> bool:
        """
        Grant a specific permission directly to a user
        
        Args:
            user (str): User identifier
            permission (str): Permission to grant
            
        Returns:
            bool: True if successful
        """
        try:
            if user not in self.permissions:
                self.permissions[user] = set()
            
            self.permissions[user].add(permission)
            logger.info(f"Permission '{permission}' granted to user '{user}'")
            return True
        except Exception as e:
            logger.error(f"Failed to grant permission: {str(e)}")
            return False
    
    def revoke_permission(self, user: str, permission: str) -> bool:
        """
        Revoke a specific permission from a user
        
        Args:
            user (str): User identifier
            permission (str): Permission to revoke
            
        Returns:
            bool: True if successful
        """
        try:
            if user in self.permissions and permission in self.permissions[user]:
                self.permissions[user].remove(permission)
                logger.info(f"Permission '{permission}' revoked from user '{user}'")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to revoke permission: {str(e)}")
            return False
    
    def check_permission(self, user: str, permission: str) -> bool:
        """
        Check if a user has a specific permission
        
        Args:
            user (str): User identifier
            permission (str): Permission to check
            
        Returns:
            bool: True if user has permission
        """
        try:
            # First check direct permissions for the user
            if user in self.permissions and permission in self.permissions[user]:
                return True
                
            # Check role-based permissions  
            if 'roles' in self.permissions and user in self.permissions['roles']:
                user_role = self.permissions['roles'][user]
                
                if user_role in self.role_permissions:
                    return permission in self.role_permissions[user_role]
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking permission for '{user}': {str(e)}")
            return False
    
    def check_user_access(self, user: str, required_permissions: list) -> Dict[str, Any]:
        """
        Check if a user has all required permissions
        
        Args:
            user (str): User identifier
            required_permissions (list): List of permissions needed
            
        Returns:
            dict: Access check results
        """
        try:
            missing_permissions = []
            granted_permissions = []
            
            for permission in required_permissions:
                if self.check_permission(user, permission):
                    granted_permissions.append(permission)
                else:
                    missing_permissions.append(permission)
            
            return {
                'user': user,
                'access_granted': len(missing_permissions) == 0,
                'granted_permissions': granted_permissions,
                'missing_permissions': missing_permissions,
                'total_required': len(required_permissions),
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Error checking user access for '{user}': {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }

# Main instance for system use
access_control = AccessControlManager()
