"""
validation.py - Input validation and sanitization for RK-OS security framework
"""

import re
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class InputValidator:
    """
    Comprehensive input validation and sanitization system
    """
    
    def __init__(self):
        """Initialize the input validator"""
        self.validation_rules = {}
        
        # Predefined validation patterns
        self.patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\+?1?-?\.?\s?$?(\d{3})$?[-.\s]?(\d{3})[-.\s]?(\d{4})$',
            'url': r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$',
            'ip_address': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
            'uuid': r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        }
        
        logger.info("Input Validator initialized")
    
    def add_validation_rule(self, field_name: str, rule_type: str, 
                           pattern: str = None, min_length: int = 0,
                           max_length: int = float('inf'), required: bool = False) -> bool:
        """
        Add a custom validation rule
        
        Args:
            field_name (str): Name of the field to validate
            rule_type (str): Type of validation ('string', 'number', 'regex', etc.)
            pattern (str): Regex pattern for validation
            min_length (int): Minimum length requirement  
            max_length (int): Maximum length requirement
            required (bool): Whether field is required
            
        Returns:
            bool: True if successful
        """
        try:
            self.validation_rules[field_name] = {
                'type': rule_type,
                'pattern': pattern,
                'min_length': min_length,
                'max_length': max_length,
                'required': required
            }
            
            logger.info(f"Added validation rule for field '{field_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add validation rule for '{field_name}': {str(e)}")
            return False
    
    def validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input data against defined rules
        
        Args:
            data (Dict): Input data to validate
            
        Returns:
            dict: Validation results
        """
        try:
            validation_results = {
                'valid': True,
                'errors': [],
                'validated_data': {}
            }
            
            # Check required fields first
            for field_name, rules in self.validation_rules.items():
                if rules['required'] and field_name not in data:
                    error_msg = f"Required field '{field_name}' is missing"
                    validation_results['valid'] = False
                    validation_results['errors'].append({
                        'field': field_name,
                        'error': error_msg,
                        'type': 'missing'
                    })
                    continue
                
                if field_name in data:
                    # Validate the value
                    value = data[field_name]
                    result = self._validate_field(field_name, value, rules)
                    
                    if not result['valid']:
                        validation_results['valid'] = False
                        validation_results['errors'].extend(result['errors'])
                    else:
                        validation_results['validated_data'][field_name] = value
            
            # Add any remaining validated data that wasn't in the rule set  
            for field_name, value in data.items():
                if field_name not in self.validation_rules:
                    validation_results['validated_data'][field_name] = value
                    
            return validation_results
            
        except Exception as e:
            logger.error(f"Failed to validate input: {str(e)}")
            return {
                'valid': False,
                'errors': [f'Validation error: {str(e)}'],
                'timestamp': time.time()
            }
    
    def _validate_field(self, field_name: str, value: Any, rules: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single field against its rules
        
        Args:
            field_name (str): Name of the field
            value (Any): Value to validate
            rules (Dict): Validation rules for this field
            
        Returns:
            dict: Validation result
        """
        try:
            errors = []
            
            # Type checking
            if rules['type'] == 'string' and not isinstance(value, str):
                errors.append({
                    'field': field_name,
                    'error': f"Field '{field_name}' must be a string",
                    'type': 'type'
                })
                return {
                    'valid': False,
                    'errors': errors
                }
            
            # Length validation for strings
            if isinstance(value, str) and len(value) < rules['min_length']:
                errors.append({
                    'field': field_name,
                    'error': f"Field '{field_name}' must be at least {rules['min_length']} characters long",
                    'type': 'length'
                })
            
            if isinstance(value, str) and len(value) > rules['max_length']:
                errors.append({
                    'field': field_name,
                    'error': f"Field '{field_name}' must not exceed {rules['max_length']} characters",
                    'type': 'length'
                })
            
            # Pattern validation
            if rules['pattern'] is not None and isinstance(value, str):
                pattern = self.patterns.get(rules['pattern'], rules['pattern'])
                if not re.match(pattern, value):
                    errors.append({
                        'field': field_name,
                        'error': f"Field '{field_name}' does not match expected format",
                        'type': 'format'
                    })
            
            # Check for any errors
            valid = len(errors) == 0
            
            return {
                'valid': valid,
                'errors': errors if errors else []
            }
            
        except Exception as e:
            logger.error(f"Failed to validate field '{field_name}': {str(e)}")
            return {
                'valid': False,
                'errors': [{
                    'field': field_name,
                    'error': f'Validation error: {str(e)}',
                    'type': 'internal'
                }]
            }
    
    def sanitize_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize input data to remove potentially dangerous content
        
        Args:
            data (Dict): Input data to sanitize
            
        Returns:
            dict: Sanitized data
        """
        try:
            sanitized_data = {}
            
            for key, value in data.items():
                if isinstance(value, str):
                    # Remove potentially dangerous characters/sequences
                    sanitized_value = self._sanitize_string(value)
                else:
                    sanitized_value = value
                    
                sanitized_data[key] = sanitized_value
                
            return sanitized_data
            
        except Exception as e:
            logger.error(f"Failed to sanitize input: {str(e)}")
            return data
    
    def _sanitize_string(self, text: str) -> str:
        """
        Sanitize a string by removing potentially dangerous content
        
        Args:
            text (str): Text to sanitize
            
        Returns:
            str: Sanitized text
        """
        try:
            # Remove common dangerous patterns
            dangerous_patterns = [
                r'<script[^>]*>.*?</script>',  # JavaScript tags
                r'javascript:',               # JavaScript protocol  
                r'on\w+\s*=',                 # Event handlers
                r'<iframe[^>]*>.*?</iframe>'   # Iframe tags
            ]
            
            sanitized_text = text
            
            for pattern in dangerous_patterns:
                sanitized_text = re.sub(pattern, '', sanitized_text, flags=re.IGNORECASE | re.DOTALL)
                
            return sanitized_text.strip()
            
        except Exception as e:
            logger.error(f"Failed to sanitize string: {str(e)}")
            return text

# Main instance for system use
input_validator = InputValidator()

# Example usage
if __name__ == "__main__":
    # Add validation rules
    input_validator.add_validation_rule('email', 'string', pattern='email', min_length=5, max_length=100, required=True)
    input_validator.add_validation_rule('age', 'number', min_length=0, max_length=120, required=True)
    
    # Test validation
    test_data = {
        'email': 'user@example.com',
        'age': 30
    }
    
    result = input_validator.validate_input(test_data)
    print(f"Validation result: {result}")
