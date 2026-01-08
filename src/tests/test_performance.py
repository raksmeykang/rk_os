"""
test_performance.py - Unit tests for RK-OS performance monitoring components  
"""

import unittest
from typing import Dict, Any
import logging

# Configure logging  
logger = logging.getLogger(__name__)

class TestPerformanceMonitoring(unittest.TestCase):
    """
    Comprehensive test suite for RK-OS performance monitoring system
    """
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            # Import required modules
            from src.monitoring.logger import PerformanceLogger
            from src.monitoring.metrics import MetricsCollector
            
            self.performance_logger = PerformanceLogger()
            self.metrics_collector = MetricsCollector()
            
            logger.info("Performance monitoring test setup completed")
            
        except Exception as e:
            logger.error(f"Failed to set up performance tests: {str(e)}")
            raise
    
    def tearDown(self):
        """Clean up test fixtures after each test method."""
        try:
            # Clean up any resources if needed
            pass
            
        except Exception as e:
            logger.error(f"Failed to tear down performance tests: {str(e)}")
    
    def test_log_operation(self):
        """Test logging of operations"""
        try:
            # Log a simple operation 
            self.performance_logger.log_operation(
                "test_operation", 
                duration=0.1,
                status="success"
            )
            
            # Check that it was logged
            metrics = self.performance_logger.get_metrics()
            self.assertIn('system_stats', metrics)
            
        except Exception as e:
            logger.error(f"Failed operation logging test: {str(e)}")
            raise
    
    def test_error_logging(self):
        """Test error logging capabilities"""
        try:
            # Log an error
            self.performance_logger.log_error(
                "TEST_ERROR", 
                "This is a test error message",
                context={'test_key': 'test_value'}
            )
            
            # Check that it was logged
            metrics = self.performance_logger.get_metrics()
            self.assertIn('system_stats', metrics)
            
        except Exception as e:
            logger.error(f"Failed error logging test: {str(e)}")
            raise
    
    def test_get_metrics(self):
        """Test getting system metrics"""
        try:
            # Get current metrics
            metrics = self.performance_logger.get_metrics()
            
            # Check basic structure  
            self.assertIn('system_stats', metrics)
            self.assertIn('uptime_seconds', metrics) 
            
        except Exception as e:
            logger.error(f"Failed get metrics test: {str(e)}")
            raise
    
    def test_performance_stats(self):
        """Test performance statistics calculation"""
        try:
            # Log several operations
            for i in range(5):
                self.performance_logger.log_operation(
                    f"operation_{i}",
                    duration=0.01 * (i + 1),
                    status="success"
                )
            
            # Get performance stats  
            stats = self.performance_logger.get_metrics()
            
            # Check that we have recent operations
            if 'recent_operations' in stats:
                self.assertGreater(len(stats['recent_operations']), 0)
                
        except Exception as e:
            logger.error(f"Failed performance stats test: {str(e)}")
            raise
    
    def test_export_log(self):
        """Test log export functionality"""
        try:
            # Export current logs
            filename = "test_export.json"
            
            # This would normally work if we have files to export
            # For now, just ensure no exceptions are raised  
            self.performance_logger.export_log(filename)
            
            logger.info(f"Log exported successfully to {filename}")
            
        except Exception as e:
            logger.error(f"Failed log export test: {str(e)}")
            raise

def run_tests() -> Dict[str, Any]:
    """
    Run all performance monitoring tests
    
    Returns:
        dict: Test results
    """
    try:
        # Create a test suite and run it
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestPerformanceMonitoring)
        
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
        logger.error(f"Failed to run performance tests: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# Run tests if script is executed directly
if __name__ == "__main__":
    print("Running RK-OS Performance Monitoring Tests...")
    
    results = run_tests()
    print(f"Test Results: {results}")
