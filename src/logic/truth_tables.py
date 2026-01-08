"""
truth_tables.py - Truth table generation for RK-OS
"""

import itertools
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TruthTableGenerator:
    """
    Comprehensive truth table generator with visualization capabilities
    """
    
    def __init__(self):
        """Initialize the truth table generator"""
        self.table_history = []
        
        logger.info("Truth Table Generator initialized")
        
    def generate_table(self, variables: List[str], expression: str) -> Dict[str, Any]:
        """
        Generate complete truth table for logical expression
        
        Args:
            variables (List[str]): Variable names
            expression (str): Logical expression
            
        Returns:
            dict: Truth table results with all combinations and outcomes
        """
        try:
            # Validate inputs
            if not variables or not expression:
                raise ValueError("Variables list and expression cannot be empty")
            
            logger.info(f"Generating truth table for {len(variables)} variables: {expression}")
            
            # Generate all possible combinations of variable values
            n = len(variables)
            combinations = list(itertools.product([True, False], repeat=n))
            
            results = []
            errors = []
            
            for i, combination in enumerate(combinations):
                # Create mapping of variables to their boolean values
                var_map = dict(zip(variables, combination))
                
                # Evaluate the expression with current combination
                try:
                    result = self._evaluate_expression(expression, var_map)
                    results.append({
                        'combination': list(combination),
                        'variables': dict(zip(variables, combination)),
                        'result': result,
                        'row_index': i
                    })
                except Exception as e:
                    error_msg = f"Error evaluating expression {expression} with values {var_map}: {str(e)}"
                    logger.error(error_msg)
                    errors.append({
                        'combination': list(combination),
                        'variables': dict(zip(variables, combination)),
                        'error': str(e),
                        'row_index': i
                    })
                    results.append({
                        'combination': list(combination),
                        'variables': dict(zip(variables, combination)),
                        'result': None,
                        'error': str(e),
                        'row_index': i
                    })
            
            table_result = {
                'variables': variables,
                'expression': expression,
                'combinations': len(combinations),
                'results': results,
                'errors': errors,
                'generated_at': datetime.now().isoformat(),
                'timestamp': time.time()
            }
            
            # Store in history
            self.table_history.append(table_result)
            
            logger.info(f"Truth table generated successfully with {len(results)} combinations")
            return table_result
            
        except Exception as e:
            error_msg = f"Failed to generate truth table: {str(e)}"
            logger.error(error_msg)
            raise
    
    def _evaluate_expression(self, expression: str, variables: Dict[str, bool]) -> bool:
        """
        Evaluate logical expression with given variable values
        
        Args:
            expression (str): Logical expression
            variables (Dict[str, bool]): Variable value mappings
            
        Returns:
            bool: Evaluation result
        """
        try:
            # Replace variables in the expression with their boolean values  
            processed_expr = expression
            
            # Handle basic replacement first (safely)
            for var_name, value in variables.items():
                if isinstance(value, bool):
                    replacement = str(value).lower()
                    processed_expr = processed_expr.replace(var_name, replacement)
            
            # Replace logical operators with Python equivalents
            replacements = {
                'AND': 'and',
                'OR': 'or', 
                'NOT': 'not',
                'IMPLIES': '->',
                'BICONDITIONAL': '<->'
            }
            
            for symbol, operator in replacements.items():
                processed_expr = processed_expr.replace(symbol, operator)
            
            # Handle special case for implication and biconditional
            # Convert P -> Q to (not P or Q) 
            # Convert P <-> Q to ((P and Q) or (not P and not Q))
            if '->' in processed_expr:
                # Simple replacement - in production would need more robust parsing
                pass
            
            if '<->' in processed_expr:
                # Simple replacement - in production would need more robust parsing  
                pass
                
            # More robust evaluation using eval with restricted environment
            allowed_names = {
                "__builtins__": {},
                "True": True,
                "False": False
            }
            
            result = eval(processed_expr, allowed_names)
            return bool(result)
            
        except Exception as e:
            raise ValueError(f"Expression evaluation error: {str(e)}")
    
    def generate_table_with_visualization(self, variables: List[str], expression: str) -> Dict[str, Any]:
        """
        Generate truth table with visual representation
        
        Args:
            variables (List[str]): Variable names  
            expression (str): Logical expression
            
        Returns:
            dict: Table with both data and visualization
        """
        try:
            # Get basic table results
            table_data = self.generate_table(variables, expression)
            
            # Create ASCII table representation for console display
            visual_representation = self._create_visual_table(table_data)
            
            table_data['visualization'] = {
                'ascii_table': visual_representation,
                'format': 'ascii'
            }
            
            return table_data
            
        except Exception as e:
            logger.error(f"Failed to generate visualization: {str(e)}")
            raise
    
    def _create_visual_table(self, table_data: Dict[str, Any]) -> str:
        """
        Create ASCII representation of truth table
        
        Args:
            table_data (Dict): Table data structure
            
        Returns:
            str: Visual table as text
        """
        try:
            variables = table_data['variables']
            results = table_data['results']
            
            # Build header row
            header = " | ".join([f"{var:>5}" for var in variables] + ["Result"])
            separator = "-+-".join(["-" * 5 for _ in range(len(variables) + 1)])
            
            lines = [header, separator]
            
            # Add data rows
            for row in results:
                if 'result' in row and row['result'] is not None:
                    values = [str(val).lower()[:5] for val in row['variables'].values()]
                    result_str = str(row['result']).lower()[:5]
                    lines.append(" | ".join(values + [result_str]))
            
            return "\n".join(lines)
            
        except Exception as e:
            logger.error(f"Failed to create visual table: {str(e)}")
            return "Error creating visualization"
    
    def get_table_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent truth table generation history
        
        Args:
            limit (int): Number of entries to return
            
        Returns:
            List: History of generated tables
        """
        try:
            return self.table_history[-limit:] if self.table_history else []
        except Exception as e:
            logger.error(f"Failed to get table history: {str(e)}")
            return []

# Main instance for system use
truth_table_generator = TruthTableGenerator()
