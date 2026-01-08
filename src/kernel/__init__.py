"""
Kernel package initialization for RK-OS
"""

__version__ = "1.0.0"
__author__ = "RK-OS Team"

# Import kernel components at package level if needed
from .bridge import KernelBridge
from .manager import ResourceManager
from .resources import ResourceHandler
from .process import ProcessManager

__all__ = [
    'KernelBridge',
    'ResourceManager', 
    'ResourceHandler',
    'ProcessManager'
]
