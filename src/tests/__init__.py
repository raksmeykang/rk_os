"""
Tests package initialization for RK-OS
"""

__version__ = "1.0.0"
__author__ = "RK-OS Team"

# Import test components at package level if needed
from .test_logic_system import run_tests as run_logic_tests
from .test_kernel_integration import run_tests as run_kernel_tests  
from .test_performance import run_tests as run_performance_tests

__all__ = [
    'run_logic_tests',
    'run_kernel_tests', 
    'run_performance_tests'
]
