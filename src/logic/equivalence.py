"""
equivalence.py - Logical equivalence checking for RK-OS
"""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

class EquivalenceChecker:
    """
    Advanced logical equivalence checker system
    """
    
    def __init__(self):
        """Initialize the equivalence checker"""
        self.checking_history = []
        
        logger.info("Equivalence Checker initialized")
        
    def check_equivalence(self, expr1: str, expr2: str, variables: List[str]) -> Dict[str, Any]:
        """
        Check if two logical expressions are equivalent
        
        Args:
            expr1 (str): First expression
            expr2 (str): Second expression  
            variables (List[str]): Variable names
            
        Returns:
            dict: Equivalence check results with confidence level
        """
        try:
            logger.info(f"Checking equivalence between '{expr1}' and '{expr2}'")
            
            # Generate truth tables for both expressions
            from src.logic.truth_tables import truth_table_generator
            
            table1 = truth_table_generator.generate_table(variables, expr1)
            table2 = truth_table_generator.generate_table(variables, expr2)
            
            # Compare results for each combination
            equivalent = True
            differences = []
            
            for i in range(len(table1['results'])):
                result1 = table1['results'][i]['result']
                result2 = table2['results'][i]['result']
                
                if result1 != result2 and result1 is not None and result2 is not None:
                    equivalent = False
                    differences.append({
                        'combination': i,
                        'expr1_result': result1,
                        'expr2_result': result2
                    })
            
            # Calculate confidence level based on number of matching combinations
            total_combinations = len(table1['results'])
            matched_combinations = total_combinations - len(differences)
            confidence = (matched_combinations / total_combinations) * 100 if total_combinations > 0 else 0
            
            check_result = {
                'expression1': expr1,
                'expression2': expr2,
                'variables': variables,
                'are_equivalent': equivalent,
                'confidence_level': confidence,
                'differences_found': len(differences),
                'differences': differences if differences else [],
                'combinations_checked': total_combinations,
                'checked_at': datetime.now().isoformat(),
                'timestamp': time.time()
            }
            
            # Store in history
            self.checking_history.append(check_result)
            
            logger.info(f"Equivalence check result: {check_result}")
            return check_result
            
        except Exception as e:
            error_msg = f"Failed to check equivalence: {str(e)}"
            logger.error(error_msg)
            raise
    
    def get_checking_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent checking history
        
        Args:
            limit (int): Number of entries to return
            
        Returns:
            List: History of checks
        """
        try:
            return self.checking_history[-limit:] if self.checking_history else []
        except Exception as e:
            logger.error(f"Failed to get checking history: {str(e)}")
            return []

# Main instance for system use  
equivalence_checker = EquivalenceChecker()
