"""
helpers.py - General utility functions for RK-OS system
"""

import time
from typing import Dict, Any, Optional, Callable
import logging

# Configure logging
logger = logging.getLogger(__name__)

class UtilityHelper:
    """
    Collection of general utility helper functions for RK-OS
    """
    
    @staticmethod
    def format_timestamp(timestamp: float = None) -> str:
        """
        Format timestamp into readable string
        
        Args:
            timestamp (float): Unix timestamp
            
        Returns:
            str: Formatted time string
        """
        try:
            if timestamp is None:
                timestamp = time.time()
                
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            
        except Exception as e:
            logger.error(f"Failed to format timestamp: {str(e)}")
            return str(timestamp)
    
    @staticmethod
    def calculate_uptime(start_time: float) -> float:
        """
        Calculate system uptime in seconds
        
        Args:
            start_time (float): System start time
            
        Returns:
            float: Uptime in seconds
        """
        try:
            current_time = time.time()
            return current_time - start_time
            
        except Exception as e:
            logger.error(f"Failed to calculate uptime: {str(e)}")
            return 0.0
    
    @staticmethod
    def bytes_to_human_readable(bytes_value: int) -> str:
        """
        Convert bytes to human readable format
        
        Args:
            bytes_value (int): Size in bytes
            
        Returns:
            str: Human readable size string
        """
        try:
            if bytes_value < 1024:
                return f"{bytes_value} B"
            
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes_value < 1024.0:
                    return f"{bytes_value:.2f} {unit}"
                bytes_value /= 1024.0
                
            return f"{bytes_value:.2f} PB"
            
        except Exception as e:
            logger.error(f"Failed to convert bytes: {str(e)}")
            return str(bytes_value)
    
    @staticmethod
    def safe_get(dictionary: Dict[str, Any], key_path: str, default=None) -> Any:
        """
        Safely get nested dictionary values using dot notation
        
        Args:
            dictionary (Dict): Source dictionary  
            key_path (str): Dot-separated path to value (e.g., 'a.b.c')
            default: Default value if not found
            
        Returns:
            Any: Value at the specified path or default
        """
        try:
            keys = key_path.split('.')
            current = dictionary
            
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return default
                    
            return current
            
        except Exception as e:
            logger.error(f"Failed to safely get value: {str(e)}")
            return default
    
    @staticmethod
    def validate_config(config_data: Dict[str, Any]) -> bool:
        """
        Validate configuration data structure
        
        Args:
            config_data (Dict): Configuration to validate
            
        Returns:
            bool: True if valid
        """
        try:
            # Basic validation checks
            required_fields = ['version', 'name']
            
            for field in required_fields:
                if field not in config_data:
                    logger.warning(f"Missing required configuration field: {field}")
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate config: {str(e)}")
            return False

# Main utility helper instance
utility_helper = UtilityHelper()

# Example usage
if __name__ == "__main__":
    print("Utility Helper Examples:")
    
    # Test timestamp formatting
    current_timestamp = time.time()
    formatted_time = utility_helper.format_timestamp(current_timestamp)
    print(f"Formatted time: {formatted_time}")
    
    # Test bytes conversion  
    readable_size = utility_helper.bytes_to_human_readable(1024 * 1024)
    print(f"Readable size: {readable_size}")
    
    # Test nested access
    test_dict = {
        'system': {
            'info': {
                'name': 'RK-OS',
                'version': '1.0.0'
            }
        }
    }
    
    name = utility_helper.safe_get(test_dict, 'system.info.name')
    print(f"Nested value: {name}")
