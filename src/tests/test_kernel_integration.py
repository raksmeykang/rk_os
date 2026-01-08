"""
test_kernel_integration.py - Unit tests for RK-OS kernel integration components
"""

import unittest
from typing import Dict, Any
import logging

# Configure logging  
logger = logging.getLogger(__name__)

class TestKernelIntegration(unittest.TestCase):
    """
    Comprehensive test suite for RK-OS kernel integration system
    """
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            # Import required modules
            from src.kernel.bridge import KernelBridge
            
            self.kernel_bridge = KernelBridge()
            
            logger.info("Kernel integration test setup completed")
            
        except Exception as e:
            logger.error(f"Failed to set up kernel tests: {str(e)}")
            raise
    
    def tearDown(self):
        """Clean up test fixtures after each test method."""
        try:
            # Clean up any resources if needed
            pass
            
        except Exception as e:
            logger.error(f"Failed to tear down kernel tests: {str(e)}")
    
    def test_system_info_collection(self):
        """Test system information collection"""
        try:
            info = self.kernel_bridge.get_system_info()
            
            # Check basic structure
            self.assertIn('success', info)
            self.assertTrue(info['success'])
            self.assertIn('system_info', info)
            self.assertIn('resource_usage', info)
            
        except Exception as e:
            logger.error(f"Failed system info test: {str(e)}")
            raise
    
    def test_resource_monitoring(self):
        """Test resource monitoring capabilities"""
        try:
            resources = self.kernel_bridge.get_system_resources()
            
            # Check basic structure
            self.assertIn('cpu_percent', resources)
            self.assertIn('memory_total', resources) 
            self.assertIn('disk_total', resources)
            
        except Exception as e:
            logger.error(f"Failed resource monitoring test: {str(e)}")
            raise
    
    def test_process_management(self):
        """Test process management capabilities"""
        try:
            # Test getting process list
            processes = self.kernel_bridge.execute_system_call("get_process_list")
            
            # Should be successful
            self.assertIn('success', processes)
            if processes['success']:
                self.assertIn('processes', processes) 
                
        except Exception as e:
            logger.error(f"Failed process management test: {str(e)}")
            raise
    
    def test_disk_usage(self):
        """Test disk usage monitoring"""
        try:
            disk_info = self.kernel_bridge.execute_system_call("get_disk_usage")
            
            # Check basic structure
            self.assertIn('success', disk_info)
            if disk_info['success']:
                self.assertIn('total', disk_info)  
                self.assertIn('used', disk_info)
                
        except Exception as e:
            logger.error(f"Failed disk usage test: {str(e)}")
            raise
    
    def test_network_monitoring(self):
        """Test network information collection"""
        try:
            # Test getting network info (if available)
            try:
                net_info = self.kernel_bridge.execute_system_call("get_network_info") 
                
                if 'success' in net_info and net_info['success']:
                    self.assertIn('total_connections', net_info)
                    
            except Exception:
                # Network monitoring might not be supported on all systems
                logger.info("Network monitoring test skipped (not available)")
                pass
                
        except Exception as e:
            logger.error(f"Failed network monitoring test: {str(e)}")
            raise

def run_tests() -> Dict[str, Any]:
    """
    Run all kernel integration tests
    
    Returns:
        dict: Test results
    """
    try:
        # Create a test suite and run it
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestKernelIntegration)
        
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
        logger.error(f"Failed to run kernel tests: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# Run tests if script is executed directly
if __name__ == "__main__":
    print("Running RK-OS Kernel Integration Tests...")
    
    results = run_tests()
    print(f"Test Results: {results}")
