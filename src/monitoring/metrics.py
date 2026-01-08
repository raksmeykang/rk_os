"""
metrics.py - Metrics collection system for RK-OS monitoring
"""

import time
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

class MetricsCollector:
    """
    System metrics collector that gathers and analyzes performance data
    """
    
    def __init__(self):
        """Initialize the metrics collector"""
        self.metrics_data = {
            'system': {},
            'cpu': [],
            'memory': [],
            'disk': [],
            'network': []
        }
        
        # Performance statistics
        self.performance_stats = {
            'operation_count': 0,
            'avg_response_time': 0.0,
            'peak_memory_usage': 0.0,
            'total_errors': 0,
            'uptime_seconds': 0.0
        }
        
        logger.info("Metrics Collector initialized")
    
    def collect_system_metrics(self) -> Dict[str, Any]:
        """
        Collect comprehensive system metrics
        
        Returns:
            dict: Collected system metrics
        """
        try:
            import psutil
            
            # System information
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Network statistics  
            net_io = psutil.net_io_counters()
            
            # Process information
            active_processes = len(psutil.process_iter(['pid']))
            
            metrics = {
                'timestamp': time.time(),
                'system_info': {
                    'cpu_percent': cpu_percent,
                    'memory_total': memory.total,
                    'memory_available': memory.available,
                    'memory_used': memory.used,
                    'memory_percent': memory.percent,
                    'disk_total': disk.total,
                    'disk_used': disk.used,
                    'disk_free': disk.free,
                    'disk_percent': disk.percent,
                    'network_bytes_sent': net_io.bytes_sent,
                    'network_bytes_recv': net_io.bytes_recv,
                    'active_processes': active_processes
                }
            }
            
            # Store for analysis
            self.metrics_data['cpu'].append(cpu_percent)
            self.metrics_data['memory'].append(memory.percent)
            
            # Keep only recent data (last 100 readings)
            if len(self.metrics_data['cpu']) > 100:
                self.metrics_data['cpu'] = self.metrics_data['cpu'][-100:]
                self.metrics_data['memory'] = self.metrics_data['memory'][-100:]
            
            # Update performance stats
            self.performance_stats['operation_count'] += 1
            if cpu_percent > self.performance_stats['peak_memory_usage']:
                self.performance_stats['peak_memory_usage'] = cpu_percent
                
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics
        
        Returns:
            dict: Performance analysis data
        """
        try:
            # Calculate averages for recent metrics
            avg_cpu = sum(self.metrics_data['cpu']) / len(self.metrics_data['cpu']) if self.metrics_data['cpu'] else 0.0
            avg_memory = sum(self.metrics_data['memory']) / len(self.metrics_data['memory']) if self.metrics_data['memory'] else 0.0
            
            # Calculate overall statistics  
            total_operations = self.performance_stats['operation_count']
            uptime_seconds = time.time() - self._get_start_time()
            
            return {
                'success': True,
                'average_cpu_percent': avg_cpu,
                'average_memory_percent': avg_memory,
                'total_operations_processed': total_operations,
                'peak_memory_usage': self.performance_stats['peak_memory_usage'],
                'total_errors': self.performance_stats['total_errors'],
                'uptime_seconds': uptime_seconds,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to get performance stats: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def _get_start_time(self) -> float:
        """Get system start time"""
        try:
            # This is a placeholder - would use actual system boot time in real implementation
            return 0.0  
        except Exception as e:
            logger.error(f"Failed to get start time: {str(e)}")
            return 0.0
    
    def add_metric(self, category: str, name: str, value: Any) -> bool:
        """
        Add a custom metric
        
        Args:
            category (str): Metric category
            name (str): Metric name  
            value (Any): Metric value
            
        Returns:
            bool: True if successful
        """
        try:
            if category not in self.metrics_data:
                self.metrics_data[category] = {}
            
            self.metrics_data[category][name] = {
                'value': value,
                'timestamp': time.time()
            }
            
            logger.info(f"Added metric {name} to category {category}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add metric: {str(e)}")
            return False

# Main instance for system use
metrics_collector = MetricsCollector()
