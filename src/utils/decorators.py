"""
decorators.py - Performance and error handling decorators for RK-OS system
"""

import time
from functools import wraps
from typing import Callable, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

def performance_monitor(func: Callable) -> Callable:
    """
    Decorator to monitor function execution performance
    
    Args:
        func (Callable): Function to decorate
        
    Returns:
        Callable: Wrapped function with performance monitoring
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            logger.info(f"Function '{func.__name__}' executed in {execution_time:.4f}s")
            
            return result
            
        except Exception as e:
            end_time = time.time() 
            execution_time = end_time - start_time
            
            logger.error(f"Function '{func.__name__}' failed after {execution_time:.4f}s: {str(e)}")
            raise
            
    return wrapper

def retry_on_failure(max_retries: int = 3, delay: float = 1.0) -> Callable:
    """
    Decorator to retry function execution on failure
    
    Args:
        max_retries (int): Maximum number of retries
        delay (float): Delay between retries in seconds
        
    Returns:
        Callable: Decorated function with retry logic
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Function '{func.__name__}' failed on attempt {attempt + 1}: {str(e)}")
                    
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                        continue
                    
            # If we get here, all retries failed
            logger.error(f"All {max_retries} attempts failed for function '{func.__name__}'")
            raise last_exception
            
        return wrapper
    
    return decorator

# Example usage  
if __name__ == "__main__":
    @performance_monitor
    def example_function():
        """Example function to demonstrate performance monitoring"""
        time.sleep(0.1)  # Simulate work
        return "Function completed"
    
    print("Running decorated function...")
    result = example_function()
    print(f"Result: {result}")
