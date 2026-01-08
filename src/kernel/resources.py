"""
resources.py - System resource handling for RK-OS kernel integration
"""

import psutil
import time
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ResourceHandler:
    """
    Handles system resource monitoring and management tasks
    """
    
    def __init__(self):
        """Initialize the resource handler"""
        self.monitoring_enabled = True
        self.resource_stats = {
            'cpu': [],
            'memory': [],
            'disk': []
        }
        
        logger.info("Resource Handler initialized")
        
    def monitor_system_resources(self, interval: float = 1.0) -> Dict[str, Any]:
        """
        Monitor system resources continuously
        
        Args:
            interval (float): Monitoring interval in seconds
            
        Returns:
            dict: Resource usage statistics
        """
        try:
            if not self.monitoring_enabled:
                return {
                    'success': False,
                    'error': 'Monitoring is disabled',
                    'timestamp': time.time()
                }
            
            # Collect current resource usage
            cpu_percent = psutil.cpu_percent(interval=interval)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Get process information
            active_processes = len(psutil.process_iter(['pid']))
            
            # Store statistics for analysis
            self.resource_stats['cpu'].append(cpu_percent)
            self.resource_stats['memory'].append(memory.percent)
            
            # Keep only recent stats (last 100 readings)  
            if len(self.resource_stats['cpu']) > 100:
                self.resource_stats['cpu'] = self.resource_stats['cpu'][-100:]
                self.resource_stats['memory'] = self.resource_stats['memory'][-100:]
            
            return {
                'success': True,
                'cpu_percent': cpu_percent,
                'memory_total': memory.total,
                'memory_available': memory.available,
                'memory_used': memory.used,
                'memory_percent': memory.percent,
                'disk_total': disk.total,
                'disk_used': disk.used,
                'disk_free': disk.free,
                'disk_percent': disk.percent,
                'active_processes': active_processes,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to monitor system resources: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def get_average_usage(self, resource_type: str) -> Dict[str, Any]:
        """
        Get average usage statistics for a resource type
        
        Args:
            resource_type (str): Resource type to analyze
            
        Returns:
            dict: Average usage statistics
        """
        try:
            if resource_type not in self.resource_stats:
                return {
                    'success': False,
                    'error': f"Unknown resource type: {resource_type}",
                    'timestamp': time.time()
                }
            
            values = self.resource_stats[resource_type]
            if not values:
                return {
                    'success': True,
                    'average': 0.0,
                    'min': 0.0,
                    'max': 0.0,
                    'count': 0,
                    'timestamp': time.time()
                }
            
            average = sum(values) / len(values)
            minimum = min(values)
            maximum = max(values)
            
            return {
                'success': True,
                'average': average,
                'min': minimum,
                'max': maximum,
                'count': len(values),
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to get average usage for {resource_type}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def enable_monitoring(self):
        """Enable system monitoring"""
        self.monitoring_enabled = True
        logger.info("System monitoring enabled")
        
    def disable_monitoring(self):
        """Disable system monitoring"""  
        self.monitoring_enabled = False
        logger.info("System monitoring disabled")

# Main instance for system use
resource_handler = ResourceHandler()
