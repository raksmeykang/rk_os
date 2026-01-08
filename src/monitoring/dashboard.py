"""
dashboard.py - Analytics dashboard for RK-OS monitoring
"""

import time
from typing import Dict, Any, Optional
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

class AnalyticsDashboard:
    """
    Real-time analytics dashboard for system performance and operations
    """
    
    def __init__(self):
        """Initialize the analytics dashboard"""
        self.dashboard_data = {
            'system_status': {},
            'performance_metrics': {},
            'alerts': [],
            'logs': []
        }
        
        self.alert_thresholds = {
            'cpu_usage': 80.0,
            'memory_usage': 85.0,
            'disk_usage': 90.0
        }
        
        logger.info("Analytics Dashboard initialized")
    
    def update_dashboard(self, metrics: Dict[str, Any]) -> None:
        """
        Update dashboard with new metrics
        
        Args:
            metrics (Dict): Metrics data to display
        """
        try:
            # Store the latest metrics  
            self.dashboard_data['performance_metrics'] = metrics
            
            # Check for alerts based on thresholds
            self._check_alerts(metrics)
            
            logger.info("Dashboard updated successfully")
            
        except Exception as e:
            logger.error(f"Failed to update dashboard: {str(e)}")
    
    def _check_alerts(self, metrics: Dict[str, Any]) -> None:
        """
        Check if any alert conditions are met
        
        Args:
            metrics (Dict): Current system metrics
        """
        try:
            # Extract relevant data from metrics
            system_info = metrics.get('system_info', {})
            
            cpu_percent = system_info.get('cpu_percent', 0.0)
            memory_percent = system_info.get('memory_percent', 0.0) 
            disk_percent = system_info.get('disk_percent', 0.0)
            
            # Check CPU alert
            if cpu_percent > self.alert_thresholds['cpu_usage']:
                self._add_alert("CPU_USAGE_HIGH", f"High CPU usage: {cpu_percent:.1f}%")
                
            # Check Memory alert  
            if memory_percent > self.alert_thresholds['memory_usage']:
                self._add_alert("MEMORY_USAGE_HIGH", f"High memory usage: {memory_percent:.1f}%")
                
            # Check Disk alert
            if disk_percent > self.alert_thresholds['disk_usage']:
                self._add_alert("DISK_USAGE_HIGH", f"High disk usage: {disk_percent:.1f}%")
                
        except Exception as e:
            logger.error(f"Failed to check alerts: {str(e)}")
    
    def _add_alert(self, alert_type: str, message: str) -> None:
        """
        Add an alert to the dashboard
        
        Args:
            alert_type (str): Type of alert
            message (str): Alert message
        """
        try:
            alert = {
                'type': alert_type,
                'message': message,
                'timestamp': time.time(),
                'formatted_time': datetime.now().isoformat()
            }
            
            self.dashboard_data['alerts'].append(alert)
            
            # Keep only recent alerts (last 50)
            if len(self.dashboard_data['alerts']) > 50:
                self.dashboard_data['alerts'] = self.dashboard_data['alerts'][-50:]
                
        except Exception as e:
            logger.error(f"Failed to add alert: {str(e)}")
    
    def get_dashboard_view(self) -> Dict[str, Any]:
        """
        Get current dashboard view
        
        Returns:
            dict: Complete dashboard data
        """
        try:
            # Create a clean copy of the dashboard data
            return {
                'timestamp': time.time(),
                'dashboard_data': self.dashboard_data,
                'formatted_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get dashboard view: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def generate_report(self, period_hours: int = 24) -> Dict[str, Any]:
        """
        Generate a performance report for the specified period
        
        Args:
            period_hours (int): Time period in hours
            
        Returns:
            dict: Performance report data
        """
        try:
            # In a real implementation, this would analyze historical data
            # For now, we'll provide basic structure with sample data
            
            return {
                'report_period': f"{period_hours} hours",
                'generated_at': time.time(),
                'formatted_time': datetime.now().isoformat(),
                'summary': {
                    'total_operations': 0,
                    'average_response_time': 0.0,
                    'peak_cpu_usage': 0.0,
                    'peak_memory_usage': 0.0
                },
                'trends': [],
                'alerts_summary': len(self.dashboard_data['alerts'])
            }
            
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }

# Main instance for system use
analytics_dashboard = AnalyticsDashboard()
