"""
engine.py - Main system engine for RK-OS
"""

import time
from datetime import datetime
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class RKOSEngine:
    """
    Main system engine that coordinates all RK-OS components
    """
    
    def __init__(self):
        """Initialize the main system engine"""
        self.system_status = "INITIALIZING"
        self.start_time = datetime.now()
        self.components = {}
        
        logger.info("RK-OS Engine initialized")
        
    def initialize_system(self) -> bool:
        """Initialize all system components"""
        try:
            # Import and initialize components
            from src.logic.propositional import PropositionalLogicEngine
            from src.kernel.bridge import KernelBridge
            from src.monitoring.logger import PerformanceLogger
            from src.security.auth import SecurityManager
            from src.serialization.json_serializer import JSONSerializer
            
            self.logic_engine = PropositionalLogicEngine()
            self.kernel_bridge = KernelBridge() 
            self.performance_logger = PerformanceLogger()
            self.security_manager = SecurityManager()
            self.serializer = JSONSerializer()
            
            self.components = {
                'logic': self.logic_engine,
                'kernel': self.kernel_bridge,
                'monitoring': self.performance_logger,
                'security': self.security_manager,
                'serialization': self.serializer
            }
            
            self.system_status = "RUNNING"
            logger.info("RK-OS System initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize RK-OS: {str(e)}")
            self.system_status = "FAILED"
            return False
    
    def process_logical_operation(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Process a logical operation through the system"""
        try:
            if not self.security_manager.authenticate():
                return {
                    'success': False,
                    'error': 'Authentication failed',
                    'timestamp': time.time()
                }
            
            # Process the operation
            result = self.logic_engine.process_operation(operation, **kwargs)
            
            # Log performance
            self.performance_logger.log_operation(
                operation=operation,
                duration=result.get('execution_time', 0.0),
                status='success'
            )
            
            return {
                'success': True,
                'result': result,
                'timestamp': time.time(),
                'system_status': self.system_status
            }
            
        except Exception as e:
            logger.error(f"Logic operation failed: {str(e)}")
            self.performance_logger.log_operation(
                operation=operation,
                duration=0.0,
                status='error',
                error=str(e)
            )
            
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system performance metrics"""
        try:
            metrics = self.performance_logger.get_metrics()
            uptime = (datetime.now() - self.start_time).total_seconds()
            
            return {
                'system_status': self.system_status,
                'uptime_seconds': uptime,
                'metrics': metrics,
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Failed to retrieve system metrics: {str(e)}")
            return {'error': str(e)}
    
    def shutdown(self):
        """Gracefully shut down the system"""
        try:
            logger.info("Shutting down RK-OS System")
            self.system_status = "SHUTTING_DOWN"
            
            # Save any pending data
            if hasattr(self, 'serializer'):
                pass  # Add serialization save logic here
                
            self.system_status = "SHUTDOWN"
            logger.info("RK-OS System shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")

# Main system initialization function
def initialize_rkos():
    """Initialize and return the main RK-OS engine"""
    engine = RKOSEngine()
    if engine.initialize_system():
        return engine
    else:
        raise RuntimeError("Failed to initialize RK-OS system")
