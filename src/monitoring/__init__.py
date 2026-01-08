"""
Monitoring package initialization for RK-OS
"""

__version__ = "1.0.0"
__author__ = "RK-OS Team"

# Import monitoring components at package level if needed
from .logger import PerformanceLogger
from .metrics import MetricsCollector  
from .dashboard import AnalyticsDashboard

__all__ = [
    'PerformanceLogger',
    'MetricsCollector',
    'AnalyticsDashboard'
]
