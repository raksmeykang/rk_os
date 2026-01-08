# Package metadata
__version__ = "1.0.0"
__author__ = "KANG CHANDARARAKSMEY"
__description__ = "Core system components for RK-OS 1.0"

# Import and expose core components
from .engine import initialize_rkos, RKOSEngine
from .processor import LogicProcessor  
from .scheduler import TaskScheduler

# Package exports
__all__ = [
    'initialize_rkos',
    'RKOSEngine', 
    'LogicProcessor',
    'TaskScheduler'
]

# Package documentation
"""
RK-OS Core Package

This package contains the fundamental building blocks of the RK-OS system:

1. Engine: Main system engine with initialization and shutdown capabilities
2. Processor: Logic processing unit for complex operations  
3. Scheduler: Task scheduling and management system

The core components work together to provide the foundational infrastructure
for all other RK-OS subsystems.
"""
