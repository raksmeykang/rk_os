"""
test_security.py - Unit tests for RK-OS security components  
"""

import unittest
from typing import Dict, Any
import logging

# Configure logging  
logger = logging.getLogger(__name__)

class TestSecurity(unittest.TestCase):
    """
    Comprehensive test suite for RK-OS security system
    """
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            # Import required modules
            from src.security.auth import SecurityManager
            from src.security.access import AccessControlManager  
            from src.security.encryption import DataEncryption
            
            self.security_manager = SecurityManager()
            self.access_control = AccessControlManager() 
            self.data_encryption = DataEncryption()
            
            logger.info("Security test setup completed")
            
        except Exception as e:
            logger.error(f"Failed to set up security tests: {str(e)}")
            raise
    
    def tearDown(self):
        """Clean up test fixtures after each test method."""
        try:
            # Clean up any resources if needed
            pass
            
        except Exception as e:
            logger.error(f"Failed to tear down security tests: {str(e)}")
    
    def test_authentication_basic(self):
        """Test basic authentication functionality"""
        try:
            # Register a user first  
            success = self.security_manager.auth_manager.register_user(
                "testuser", 
                "password123",
                "admin"
            )
            
            self.assertTrue(success, "User registration should succeed")
            
            # Try authenticating
            auth_result = self.security_manager.authenticate("testuser", "password123") 
            
            self.assertIn('success', auth_result)
            if auth_result['success']:
                self.assertIn('token', auth_result)
                
        except Exception as e:
            logger.error(f"Failed authentication test: {str(e)}")
            raise
    
    def test_access_control(self):
        """Test access control functionality"""
        try:
            # Create a role
            success = self.access_control.create_role("test_role", ["read", "write"])
            
            self.assertTrue(success, "Role creation should succeed")
            
            # Assign role to user  
            assigned = self.access_control.assign_role_to_user("testuser", "test_role") 
            
            self.assertTrue(assigned, "Role assignment should succeed")
            
        except Exception as e:
            logger.error(f"Failed access control test: {str(e)}")
            raise
    
    def test_encryption_basic(self):
        """Test basic encryption functionality"""
        try:
            # Generate a key
            key = self.data_encryption.generate_encryption_key()
            
            self.assertIsInstance(key, str)
            self.assertGreater(len(key), 0)
            
            # Test simple encryption/decryption  
            data = "This is test data"
            encrypted_result = self.data_encryption.encrypt_data(data, key) 
            
            self.assertIn('success', encrypted_result)
            if encrypted_result['success']:
                self.assertIn('data', encrypted_result)
                
                # Try to decrypt
                decrypted_result = self.data_encryption.decrypt_data(
                    encrypted_result['data'], 
                    key
                )
                
                self.assertTrue(decrypted_result['success'])
                
        except Exception as e:
            logger.error(f"Failed encryption test: {str(e)}")
            raise
    
    def test_hashing(self):
        """Test data hashing functionality"""
        try:
            data = "test data for hashing"
            
            # Test SHA256 hash
            hash_result = self.data_encryption.hash_data(data, "sha256") 
            
            self.assertTrue(hash_result['success'])
            if hash_result['success']:
                self.assertIn('data', hash_result)
                
        except Exception as e:
            logger.error(f"Failed hashing test: {str(e)}")
            raise

def run_tests() -> Dict[str, Any]:
    """
    Run all security tests
    
    Returns:
        dict: Test results
    """
    try:
        # Create a test suite and run it
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestSecurity)
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return {
            'success': True,
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'successful': not (result.failures or result.errors)
        }
        
    except Exception as e:
        logger.error(f"Failed to run security tests: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# Run tests if script is executed directly
if __name__ == "__main__":
    print("Running RK-OS Security Tests...")
    
    results = run_tests()
    print(f"Test Results: {results}")
