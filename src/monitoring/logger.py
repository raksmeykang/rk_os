"""
logger.py - Performance monitoring and logging system for RK-OS
"""

import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import threading
from collections import deque

# Configure logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rkos_monitoring.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PerformanceLogger:
    """
    Comprehensive performance monitoring and logging system for RK-OS
    """
    
    def __init__(self, max_history: int = 1000):
        """Initialize the performance logger"""
        self.operation_history = deque(maxlen=max_history)
        self.metrics_history = deque(maxlen=max_history)
        self.error_log = deque(maxlen=max_history)
        self.system_stats = {
            'start_time': time.time(),
            'total_operations': 0,
            'errors_count': 0,
            'warnings_count': 0
        }
        
        # Thread safety
        self._lock = threading.Lock()
        
        logger.info("Performance Logger initialized")
    
    def log_operation(self, operation: str, duration: float, status: str = "success", 
                     error: Optional[str] = None, **kwargs) -> None:
        """
        Log a performance operation
        
        Args:
            operation (str): Name of the operation
            duration (float): Execution time in seconds
            status (str): Status of operation ("success", "error", "warning")
            error (Optional[str]): Error message if any
            **kwargs: Additional metadata about the operation
        """
        with self._lock:
            try:
                log_entry = {
                    'timestamp': time.time(),
                    'operation': operation,
                    'duration': duration,
                    'status': status,
                    'metadata': kwargs,
                    'formatted_time': datetime.now().isoformat()
                }
                
                if error:
                    log_entry['error'] = error
                    self.system_stats['errors_count'] += 1
                    
                # Add to history
                self.operation_history.append(log_entry)
                
                # Update system stats
                self.system_stats['total_operations'] += 1
                
                # Log with standard logging
                if status == "success":
                    logger.info(f"Operation '{operation}' completed in {duration:.4f}s")
                elif status == "error":
                    logger.error(f"Operation '{operation}' failed after {duration:.4f}s: {error}")
                else:
                    logger.warning(f"Operation '{operation}' with status '{status}' took {duration:.4f}s")
                    
            except Exception as e:
                logger.error(f"Failed to log operation '{operation}': {str(e)}")
    
    def log_metrics(self, metrics: Dict[str, Any], category: str = "general") -> None:
        """
        Log system metrics
        
        Args:
            metrics (Dict): Dictionary of metric values
            category (str): Category for the metrics
        """
        with self._lock:
            try:
                metrics_entry = {
                    'timestamp': time.time(),
                    'category': category,
                    'metrics': metrics,
                    'formatted_time': datetime.now().isoformat()
                }
                
                self.metrics_history.append(metrics_entry)
                
                # Log for monitoring
                metric_str = ', '.join([f"{k}: {v}" for k, v in metrics.items()])
                logger.info(f"Metrics ({category}): {metric_str}")
                
            except Exception as e:
                logger.error(f"Failed to log metrics: {str(e)}")
    
    def log_error(self, error_type: str, message: str, context: Optional[Dict] = None) -> None:
        """
        Log an error with detailed context
        
        Args:
            error_type (str): Type of error
            message (str): Error message
            context (Optional[Dict]): Additional context information
        """
        with self._lock:
            try:
                error_entry = {
                    'timestamp': time.time(),
                    'error_type': error_type,
                    'message': message,
                    'context': context or {},
                    'formatted_time': datetime.now().isoformat()
                }
                
                self.error_log.append(error_entry)
                self.system_stats['errors_count'] += 1
                
                logger.error(f"Error [{error_type}]: {message}")
                if context:
                    logger.error(f"Context: {context}")
                    
            except Exception as e:
                logger.error(f"Failed to log error: {str(e)}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current system metrics
        
        Returns:
            Dict with system statistics and recent operations
        """
        with self._lock:
            try:
                # Calculate average operation time from recent history
                if len(self.operation_history) > 0:
                    durations = [op['duration'] for op in self.operation_history]
                    avg_duration = sum(durations) / len(durations)
                    
                    # Get most recent operations
                    recent_operations = list(self.operation_history)[-10:]  # Last 10 operations
                    
                    # Count operation types
                    operation_counts = {}
                    for op in self.operation_history:
                        op_name = op['operation']
                        operation_counts[op_name] = operation_counts.get(op_name, 0) + 1
                    
                    recent_errors = list(self.error_log)[-5:] if len(self.error_log) > 0 else []
                else:
                    avg_duration = 0.0
                    recent_operations = []
                    operation_counts = {}
                    recent_errors = []
                
                # Calculate uptime
                uptime_seconds = time.time() - self.system_stats['start_time']
                
                return {
                    'system_stats': self.system_stats,
                    'uptime_seconds': uptime_seconds,
                    'average_operation_duration': avg_duration,
                    'recent_operations': recent_operations,
                    'operation_counts': operation_counts,
                    'recent_errors': recent_errors,
                    'timestamp': time.time(),
                    'formatted_time': datetime.now().isoformat()
                }
            except Exception as e:
                logger.error(f"Failed to get metrics: {str(e)}")
                return {
                    'error': str(e),
                    'timestamp': time.time()
                }
    
    def export_log(self, filename: str = None) -> str:
        """
        Export the current log data to JSON
        
        Args:
            filename (Optional[str]): Output file name
            
        Returns:
            str: Path to exported file
        """
        with self._lock:
            try:
                if not filename:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"rkos_export_{timestamp}.json"
                
                export_data = {
                    'operation_history': list(self.operation_history),
                    'metrics_history': list(self.metrics_history),
                    'error_log': list(self.error_log),
                    'system_stats': self.system_stats,
                    'exported_at': time.time(),
                    'formatted_time': datetime.now().isoformat()
                }
                
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2)
                
                logger.info(f"Log exported to {filename}")
                return filename
                
            except Exception as e:
                logger.error(f"Failed to export log: {str(e)}")
                raise
    
    def clear_logs(self) -> None:
        """Clear all logs and reset statistics"""
        with self._lock:
            try:
                self.operation_history.clear()
                self.metrics_history.clear()
                self.error_log.clear()
                
                # Reset system stats
                self.system_stats = {
                    'start_time': time.time(),
                    'total_operations': 0,
                    'errors_count': 0,
                    'warnings_count': 0
                }
                
                logger.info("Logs cleared successfully")
            except Exception as e:
                logger.error(f"Failed to clear logs: {str(e)}")
    
    def get_operation_stats(self, operation_name: str = None) -> Dict[str, Any]:
        """
        Get statistics for specific operations
        
        Args:
            operation_name (Optional[str]): Specific operation name or None for all
            
        Returns:
            Dict with operation statistics
        """
        with self._lock:
            try:
                # Filter by operation name if specified
                filtered_operations = list(self.operation_history)
                if operation_name:
                    filtered_operations = [op for op in filtered_operations 
                                        if op['operation'] == operation_name]
                
                if not filtered_operations:
                    return {
                        'operation': operation_name or "all",
                        'count': 0,
                        'total_time': 0.0,
                        'average_time': 0.0,
                        'min_time': 0.0,
                        'max_time': 0.0
                    }
                
                # Calculate statistics
                durations = [op['duration'] for op in filtered_operations]
                return {
                    'operation': operation_name or "all",
                    'count': len(durations),
                    'total_time': sum(durations),
                    'average_time': sum(durations) / len(durations),
                    'min_time': min(durations),
                    'max_time': max(durations),
                    'timestamp': time.time()
                }
            except Exception as e:
                logger.error(f"Failed to get operation stats: {str(e)}")
                return {
                    'error': str(e),
                    'timestamp': time.time()
                }

# Simple performance monitor class
class SimplePerformanceMonitor:
    """Simple performance monitoring for basic metrics"""
    
    def __init__(self):
        self.start_time = time.time()
        self.operation_times = []
        
    def start_timer(self) -> float:
        """Start a timer and return the timestamp"""
        return time.time()
    
    def end_timer(self, start_time: float, operation_name: str) -> float:
        """End timer and record duration"""
        end_time = time.time()
        duration = end_time - start_time
        self.operation_times.append({
            'operation': operation_name,
            'duration': duration,
            'timestamp': end_time
        })
        return duration

# Example usage
if __name__ == "__main__":
    # Initialize the logger
    perf_logger = PerformanceLogger()
    
    print("Performance Logger Test")
    print("=" * 30)
    
    # Log some operations
    perf_logger.log_operation("test_op_1", 0.5, "success", test_param="value")
    perf_logger.log_operation("test_op_2", 1.2, "error", error="Something went wrong")
    perf_logger.log_operation("test_op_3", 0.8, "warning", warning="This is a warning")
    
    # Log metrics
    perf_logger.log_metrics({
        'cpu_percent': 75.5,
        'memory_mb': 1245,
        'disk_usage_percent': 60.2
    }, "system_health")
    
    # Get current metrics
    metrics = perf_logger.get_metrics()
    print(f"System uptime: {metrics['uptime_seconds']:.2f} seconds")
    print(f"Total operations: {metrics['system_stats']['total_operations']}")
    print(f"Errors count: {metrics['system_stats']['errors_count']}")
    
    # Export log
    try:
        exported_file = perf_logger.export_log("test_export.json")
        print(f"Log exported to: {exported_file}")
    except Exception as e:
        print(f"Export failed: {str(e)}")
