"""
tautology.py - Tautology and contradiction detection for RK-OS
"""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TautologyDetector:
    """
    Advanced tautology and contradiction detection system
    """
    
    def __init__(self):
        """Initialize the tautology detector"""
        self.detection_history = []
        
        logger.info("Tautology Detector initialized")
        
    def detect_tautology(self, expression: str, variables: List[str]) -> Dict[str, Any]:
        """
        Detect if an expression is a tautology (always true)
        
        Args:
            expression (str): Logical expression
            variables (List[str]): Variable names
            
        Returns:
            dict: Detection results with confidence level
        """
        try:
            logger.info(f"Detecting tautology for expression: {expression}")
            
            # Generate truth table to check all combinations
            from src.logic.truth_tables import truth_table_generator
            
            table = truth_table_generator.generate_table(variables, expression)
            
            # Check if all results are true (tautology) 
            all_true = True
            all_false = True
            
            for result in table['results']:
                if 'result' in result and result['result'] is not None:
                    if result['result'] is False:
                        all_true = False
                    elif result['result'] is True:
                        all_false = False
                        
            # Determine the type of logical property
            is_tautology = all_true and len([r for r in table['results'] if 'result' in r and r['result'] is not None]) > 0
            
            # A contradiction would be when all results are false  
            is_contradiction = all_false and len([r for r in table['results'] if 'result' in r and r['result'] is not None]) > 0
            
            detection_result = {
                'expression': expression,
                'variables': variables,
                'is_tautology': is_tautology,
                'is_contradiction': is_contradiction,
                'combinations_checked': table['combinations'],
                'truth_table_results': [r['result'] for r in table['results'] if 'result' in r and r['result'] is not None],
                'detected_at': datetime.now().isoformat(),
                'timestamp': time.time()
            }
            
            # Store in history
            self.detection_history.append(detection_result)
            
            logger.info(f"Tautology detection result: {detection_result}")
            return detection_result
            
        except Exception as e:
            error_msg = f"Failed to detect tautology for '{expression}': {str(e)}"
            logger.error(error_msg)
            raise
    
    def detect_contradiction(self, expression: str, variables: List[str]) -> Dict[str, Any]:
        """
        Detect if an expression is a contradiction (always false)
        
        Args:
            expression (str): Logical expression
            variables (List[str]): Variable names
            
        Returns:
            dict: Detection results with confidence level
        """
        try:
            logger.info(f"Detecting contradiction for expression: {expression}")
            
            # Generate truth table to check all combinations  
            from src.logic.truth_tables import truth_table_generator
            
            table = truth_table_generator.generate_table(variables, expression)
            
            # Check if all results are false (contradiction)
            all_false = True
            any_true = False
            
            for result in table['results']:
                if 'result' in result and result['result'] is not None:
                    if result['result'] is True:
                        all_false = False
                        any_true = True
                        
            # Determine the type of logical property
            is_contradiction = all_false and len([r for r in table['results'] if 'result' in r and r['result'] is not None]) > 0
            
            # A tautology would be when all results are true
            is_tautology = not any_true and len([r for r in table['results'] if 'result' in r and r['result'] is not None]) > 0
            
            detection_result = {
                'expression': expression,
                'variables': variables,
                'is_contradiction': is_contradiction,
                'is_tautology': is_tautology,
                'combinations_checked': table['combinations'],
                'truth_table_results': [r['result'] for r in table['results'] if 'result' in r and r['result'] is not None],
                'detected_at': datetime.now().isoformat(),
                'timestamp': time.time()
            }
            
            # Store in history
            self.detection_history.append(detection_result)
            
            logger.info(f"Contradiction detection result: {detection_result}")
            return detection_result
            
        except Exception as e:
            error_msg = f"Failed to detect contradiction for '{expression}': {str(e)}"
            logger.error(error_msg)
            raise
    
    def check_logical_equivalence(self, expr1: str, expr2: str, variables: List[str]) -> Dict[str, Any]:
        """
        Check if two expressions are logically equivalent
        
        Args:
            expr1 (str): First expression
            expr2 (str): Second expression  
            variables (List[str]): Variable names
            
        Returns:
            dict: Equivalence check results
        """
        try:
            logger.info(f"Checking logical equivalence between '{expr1}' and '{expr2}'")
            
            # Generate truth tables for both expressions
            from src.logic.truth_tables import truth_table_generator
            
            table1 = truth_table_generator.generate_table(variables, expr1)
            table2 = truth_table_generator.generate_table(variables, expr2)
            
            # Compare results for each combination
            equivalent = True
            comparison_results = []
            
            for i in range(len(table1['results'])):
                result1 = table1['results'][i]['result']
                result2 = table2['results'][i]['result']
                
                comparison_results.append({
                    'combination': i,
                    'expr1_result': result1,
                    'expr2_result': result2,
                    'equivalent': (result1 == result2) if result1 is not None and result2 is not None else False
                })
                
                # If any combination differs, they're not equivalent
                if result1 != result2:
                    equivalent = False
                    
            detection_result = {
                'expression1': expr1,
                'expression2': expr2,
                'variables': variables,
                'are_equivalent': equivalent,
                'comparison_results': comparison_results,
                'combinations_checked': len(table1['results']),
                'detected_at': datetime.now().isoformat(),
                'timestamp': time.time()
            }
            
            # Store in history
            self.detection_history.append(detection_result)
            
            logger.info(f"Equivalence check result: {detection_result}")
            return detection_result
            
        except Exception as e:
            error_msg = f"Failed to check logical equivalence: {str(e)}"
            logger.error(error_msg)
            raise
    
    def get_detection_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent detection history
        
        Args:
            limit (int): Number of entries to return
            
        Returns:
            List: History of detections
        """
        try:
            return self.detection_history[-limit:] if self.detection_history else []
        except Exception as e:
            logger.error(f"Failed to get detection history: {str(e)}")
            return []

# Main instance for system use  
tautology_detector = TautologyDetector()
