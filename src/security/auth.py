"""
auth.py - Authentication and security framework for RK-OS
"""

import hashlib
import secrets
import time
from typing import Dict, Any, Optional
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

class SecurityError(Exception):
    """Custom exception for security-related errors"""
    pass

class AuthenticationManager:
    """
    Comprehensive authentication and authorization system for RK-OS
    """
    
    def __init__(self):
        """Initialize the authentication manager"""
        self.users = {}
        self.active_sessions = {}
        self.failed_attempts = {}
        self.max_failed_attempts = 5
        self.lockout_duration = 300  # 5 minutes in seconds
        
        logger.info("Authentication Manager initialized")
        
    def register_user(self, username: str, password: str, role: str = "user") -> bool:
        """
        Register a new user with hashed password
        
        Args:
            username (str): User identifier
            password (str): Plain text password
            role (str): User role
            
        Returns:
            bool: True if registration successful
        """
        try:
            # Hash the password using SHA-256 with salt
            salt = secrets.token_hex(16)
            hashed_password = self._hash_password(password, salt)
            
            self.users[username] = {
                'password_hash': hashed_password,
                'salt': salt,
                'role': role,
                'created_at': time.time(),
                'last_login': None
            }
            
            logger.info(f"User '{username}' registered successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register user '{username}': {str(e)}")
            raise SecurityError(f"Registration failed: {str(e)}")
    
    def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate a user
        
        Args:
            username (str): User identifier
            password (str): Plain text password
            
        Returns:
            Dict with authentication result and session info
        """
        try:
            # Check if user exists
            if username not in self.users:
                logger.warning(f"Failed authentication attempt for non-existent user: {username}")
                return {
                    'success': False,
                    'error': 'Invalid credentials',
                    'timestamp': time.time()
                }
            
            user = self.users[username]
            
            # Check account lockout
            if self._is_account_locked(username):
                logger.warning(f"Account locked for user: {username}")
                return {
                    'success': False,
                    'error': 'Account temporarily locked due to failed attempts',
                    'timestamp': time.time()
                }
            
            # Verify password
            stored_hash = user['password_hash']
            salt = user['salt']
            provided_hash = self._hash_password(password, salt)
            
            if provided_hash == stored_hash:
                # Successful authentication - reset failed attempts
                self.failed_attempts.pop(username, None)
                
                # Create session token
                session_token = secrets.token_urlsafe(32)
                expiration_time = time.time() + 3600  # 1 hour expiry
                
                self.active_sessions[session_token] = {
                    'username': username,
                    'role': user['role'],
                    'created_at': time.time(),
                    'expires_at': expiration_time
                }
                
                logger.info(f"User '{username}' authenticated successfully")
                return {
                    'success': True,
                    'token': session_token,
                    'user': {
                        'username': username,
                        'role': user['role']
                    },
                    'timestamp': time.time()
                }
            else:
                # Failed authentication - increment failed attempts
                self._record_failed_attempt(username)
                logger.warning(f"Failed authentication attempt for user: {username}")
                
                return {
                    'success': False,
                    'error': 'Invalid credentials',
                    'timestamp': time.time()
                }
                
        except Exception as e:
            logger.error(f"Authentication error for user '{username}': {str(e)}")
            raise SecurityError(f"Authentication failed: {str(e)}")
    
    def validate_session(self, token: str) -> Dict[str, Any]:
        """
        Validate a session token
        
        Args:
            token (str): Session token to validate
            
        Returns:
            Dict with validation result
        """
        try:
            if token not in self.active_sessions:
                return {
                    'success': False,
                    'error': 'Invalid or expired session',
                    'timestamp': time.time()
                }
            
            session = self.active_sessions[token]
            
            # Check expiration
            if time.time() > session['expires_at']:
                del self.active_sessions[token]  # Remove expired session
                return {
                    'success': False,
                    'error': 'Session expired',
                    'timestamp': time.time()
                }
            
            logger.info(f"Valid session token for user: {session['username']}")
            return {
                'success': True,
                'user': session['username'],
                'role': session['role'],
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Session validation error: {str(e)}")
            raise SecurityError(f"Session validation failed: {str(e)}")
    
    def logout(self, token: str) -> bool:
        """
        Logout a user by invalidating their session
        
        Args:
            token (str): Session token to invalidate
            
        Returns:
            bool: True if successful
        """
        try:
            if token in self.active_sessions:
                del self.active_sessions[token]
                logger.info("User logged out successfully")
                return True
            else:
                logger.warning("Attempted logout with invalid session token")
                return False
                
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            raise SecurityError(f"Logout failed: {str(e)}")
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """
        Change user password
        
        Args:
            username (str): User identifier
            old_password (str): Current password
            new_password (str): New password
            
        Returns:
            bool: True if successful
        """
        try:
            # First authenticate with old password
            auth_result = self.authenticate(username, old_password)
            
            if not auth_result['success']:
                raise SecurityError("Current password is incorrect")
            
            # Hash new password and update
            salt = secrets.token_hex(16)
            hashed_password = self._hash_password(new_password, salt)
            
            self.users[username]['password_hash'] = hashed_password
            self.users[username]['salt'] = salt
            
            logger.info(f"Password changed for user: {username}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to change password for '{username}': {str(e)}")
            raise SecurityError(f"Password change failed: {str(e)}")
    
    def _hash_password(self, password: str, salt: str) -> str:
        """
        Hash a password with salt
        
        Args:
            password (str): Plain text password
            salt (str): Salt value
            
        Returns:
            str: Hashed password
        """
        # Combine password and salt then hash
        combined = password + salt
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def _record_failed_attempt(self, username: str) -> None:
        """Record a failed authentication attempt"""
        if username not in self.failed_attempts:
            self.failed_attempts[username] = []
        
        self.failed_attempts[username].append(time.time())
        
        # Keep only recent attempts (within lockout period)
        cutoff_time = time.time() - self.lockout_duration
        self.failed_attempts[username] = [
            attempt for attempt in self.failed_attempts[username]
            if attempt > cutoff_time
        ]
    
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to too many failed attempts"""
        if username not in self.failed_attempts:
            return False
        
        # Check if we have exceeded max failed attempts within lockout period
        recent_attempts = [
            attempt for attempt in self.failed_attempts[username]
            if time.time() - attempt < self.lockout_duration
        ]
        
        return len(recent_attempts) >= self.max_failed_attempts
    
    def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get user information (without password details)
        
        Args:
            username (str): User identifier
            
        Returns:
            Dict with user info or None if not found
        """
        try:
            if username in self.users:
                user = self.users[username]
                return {
                    'username': username,
                    'role': user['role'],
                    'created_at': datetime.fromtimestamp(user['created_at']).isoformat(),
                    'last_login': user.get('last_login', None)
                }
            return None
        except Exception as e:
            logger.error(f"Error getting user info for '{username}': {str(e)}")
            return None
    
    def get_system_security_stats(self) -> Dict[str, Any]:
        """
        Get system security statistics
        
        Returns:
            Dict with security metrics
        """
        try:
            active_sessions_count = len(self.active_sessions)
            total_users = len(self.users)
            failed_attempts_count = sum(len(attempts) for attempts in self.failed_attempts.values())
            
            return {
                'active_sessions': active_sessions_count,
                'total_users': total_users,
                'failed_attempts': failed_attempts_count,
                'max_failed_attempts': self.max_failed_attempts,
                'lockout_duration_seconds': self.lockout_duration,
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Error getting security stats: {str(e)}")
            return {
                'error': str(e),
                'timestamp': time.time()
            }

class AccessControlManager:
    """
    Access control and authorization manager
    """
    
    def __init__(self):
        """Initialize access control system"""
        self.permissions = {}
        logger.info("Access Control Manager initialized")
        
    def grant_permission(self, user: str, permission: str) -> bool:
        """
        Grant a permission to a user
        
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
        Revoke a permission from a user
        
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
            return (
                user in self.permissions and 
                permission in self.permissions[user]
            )
        except Exception as e:
            logger.error(f"Error checking permission for '{user}': {str(e)}")
            return False

# Main security manager combining authentication and access control
class SecurityManager:
    """
    Centralized security manager for RK-OS system
    """
    
    def __init__(self):
        """Initialize the complete security system"""
        self.auth_manager = AuthenticationManager()
        self.access_control = AccessControlManager()
        
        logger.info("Security Manager initialized")
        
    def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate a user"""
        return self.auth_manager.authenticate(username, password)
    
    def validate_session(self, token: str) -> Dict[str, Any]:
        """Validate a session token"""
        return self.auth_manager.validate_session(token)
    
    def check_permission(self, user: str, permission: str) -> bool:
        """Check if user has specific permission"""
        return self.access_control.check_permission(user, permission)
    
    def get_security_stats(self) -> Dict[str, Any]:
        """Get comprehensive security statistics"""
        try:
            auth_stats = self.auth_manager.get_system_security_stats()
            return {
                'authentication': auth_stats,
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Error getting security stats: {str(e)}")
            return {'error': str(e)}

# Example usage
if __name__ == "__main__":
    # Initialize security manager
    sec_manager = SecurityManager()
    
    print("Security Manager Test")
    print("=" * 30)
    
    # Register a user
    try:
        success = sec_manager.auth_manager.register_user("testuser", "password123", "admin")
        if success:
            print("User registered successfully")
        
        # Authenticate user
        auth_result = sec_manager.authenticate("testuser", "password123")
        if auth_result['success']:
            print(f"Authentication successful, token: {auth_result['token'][:10]}...")
            
            # Check permissions  
            has_access = sec_manager.check_permission("testuser", "read_system_data")
            print(f"User has read permission: {has_access}")
        
    except Exception as e:
        print(f"Security test failed: {str(e)}")
