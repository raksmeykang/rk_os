"""
RK-OS Panel Interface Package
"""

__version__ = "1.0.0"
__author__ = "RK-OS Team"

# Import interface components at package level if needed
from .cli import CommandLineInterface
from .gui import GraphicalUserInterface
from .api import PanelServer

__all__ = [
    'CommandLineInterface',
    'GraphicalUserInterface',
    'PanelServer'
]
