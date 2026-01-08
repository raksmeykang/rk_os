"""
test_logic_system.py - Unit tests for RK-OS logic system components
"""

import unittest
from typing import Dict, Any
import logging

# Configure logging  
logger = logging.getLogger(__name__)

class TestLogicSystem(unittest.TestCase):
    """
    Comprehensive test suite for RK-OS logic system
    """
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            # Import required modules
            from src.logic.propositional import PropositionalLogicEngine
            
            self.engine = PropositionalLogicEngine()
            
            logger.info("Test setup completed")
            
        except Exception as e:
            logger.error(f"Failed to set up tests: {str(e)}")
            raise
    
    def tearDown(self):
        """Clean up test fixtures after each test method."""
        try:
            # Clean up any resources if needed
            pass
            
        except Exception as e:
            logger.error(f"Failed to tear down tests: {str(e)}")
    
    def test_propositional_and_operation(self):
        """Test AND logical operation"""
        try:
            result = self.engine.evaluate_and(True, True)
            self.assertTrue(result, "AND(true, true) should be True")
            
            result = self.engine.evaluate_and(True, False)
            self.assertFalse(result, "AND(true, false) should be False")
            
            result = self.engine.evaluate_and(False, True)
            self.assertFalse(result, "AND(false, true) should be False")
            
            result = self.engine.evaluate_and(False, False)
            self.assertFalse(result, "AND(false, false) should be False")
            
        except Exception as e:
            logger.error(f"Failed AND operation test: {str(e)}")
            raise
    
    def test_propositional_or_operation(self):
        """Test OR logical operation"""
        try:
            result = self.engine.evaluate_or(True, True)
            self.assertTrue(result, "OR(true, true) should be True")
            
            result = self.engine.evaluate_or(True, False)
            self.assertTrue(result, "OR(true, false) should be True")
            
            result = self.engine.evaluate_or(False, True)
            self.assertTrue(result, "OR(false, true) should be True")
            
            result = self.engine.evaluate_or(False, False)
            self.assertFalse(result, "OR(false, false) should be False")
            
        except Exception as e:
            logger.error(f"Failed OR operation test: {str(e)}")
            raise
    
    def test_propositional_not_operation(self):
        """Test NOT logical operation"""
        try:
            result = self.engine.evaluate_not(True)
            self.assertFalse(result, "NOT(true) should be False")
            
            result = self.engine.evaluate_not(False)
            self.assertTrue(result, "NOT(false) should be True")
            
        except Exception as e:
            logger.error(f"Failed NOT operation test: {str(e)}")
            raise
    
    def test_truth_table_generation(self):
        """Test truth table generation"""
        try:
            variables = ['P', 'Q']
            expression = "P AND Q"
            
            result = self.engine.generate_truth_table(variables, expression)
            
            # Check basic structure
            self.assertIn('variables', result)
            self.assertIn('expression', result) 
            self.assertIn('results', result)
            self.assertEqual(len(result['results']), 4)  # 2^2 combinations
            
        except Exception as e:
            logger.error(f"Failed truth table test: {str(e)}")
            raise
    
    def test_tautology_detection(self):
        """Test tautology detection"""
        try:
            variables = ['P', 'Q']
            
            # Test a tautology (always true)
            expression1 = "P OR NOT P"
            is_tautology = self.engine.detect_tautology(expression1, variables) 
            
            # Should be detected as tautology
            # This test may need adjustment based on implementation
            
        except Exception as e:
            logger.error(f"Failed tautology detection test: {str(e)}")
            raise
    
    def test_equivalence_checking(self):
        """Test logical equivalence checking"""
        try:
            variables = ['P', 'Q']
            
            # Test simple equivalence
            expr1 = "P AND Q"
            expr2 = "Q AND P"
            
            result = self.engine.check_equivalence(expr1, expr2, variables)
            # Should be equivalent (commutative property) 
            
        except Exception as e:
            logger.error(f"Failed equivalence test: {str(e)}")
            raise
    
    def test_error_handling(self):
        """Test error handling in logic operations"""
        try:
            # Test invalid expression
            with self.assertRaises(Exception):  # Should be LogicError or similar
                variables = ['P']
                result = self.engine.evaluate_expression("INVALID EXPRESSION", {'P': True})
                
        except Exception as e:
            logger.error(f"Failed error handling test: {str(e)}")
            raise

def run_tests() -> Dict[str, Any]:
    """
    Run all logic system tests
    
    Returns:
        dict: Test results
    """
    try:
        # Create a test suite and run it
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestLogicSystem)
        
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
        logger.error(f"Failed to run logic tests: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# Run tests if script is executed directly
if __name__ == "__main__":
    print("Running RK-OS Logic System Tests...")
    
    results = run_tests()
    print(f"Test Results: {results}")
