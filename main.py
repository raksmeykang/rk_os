#!/usr/bin/env python3
"""
RK-OS - Logical Operating System
Complete implementation of Logic 1.0 + 1.1 system with all core features
"""

import sys
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rkos.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class RKOS:
    """
    Main RK-OS system class that coordinates all components
    """
    
    def __init__(self):
        """Initialize the complete RK-OS system"""
        self.system_status = "INITIALIZING"
        self.components = {}
        self.start_time = datetime.now()
        
        logger.info("Initializing RK-OS System")
        
        # Import and initialize all subsystems
        try:
            from src.logic.propositional_logic import PropositionalLogicEngine
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
            
        except Exception as e:
            logger.error(f"Failed to initialize RK-OS: {str(e)}")
            self.system_status = "FAILED"
    
    def process_logic_operation(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Process a logical operation through the system
        
        Args:
            operation (str): Type of logical operation
            **kwargs: Operation parameters
            
        Returns:
            dict: Result with success status and data
        """
        try:
            logger.info(f"Processing logic operation: {operation}")
            
            # Security check first
            if not self.security_manager.authenticate():
                return {
                    'success': False,
                    'error': 'Authentication failed',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Process the operation through the logic engine
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
                'timestamp': datetime.now().isoformat(),
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
                'timestamp': datetime.now().isoformat()
            }
    
    def generate_truth_table(self, variables: list, expression: str) -> Dict[str, Any]:
        """
        Generate a truth table for logical expressions
        
        Args:
            variables (list): List of variable names
            expression (str): Logical expression
            
        Returns:
            dict: Truth table results
        """
        try:
            logger.info(f"Generating truth table for {expression}")
            
            result = self.logic_engine.generate_truth_table(variables, expression)
            
            # Log the operation
            self.performance_logger.log_operation(
                operation='truth_table_generation',
                duration=0.0,
                status='success'
            )
            
            return {
                'success': True,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Truth table generation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
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
                'timestamp': datetime.now().isoformat()
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
                self.serializer.save_system_state()
                
            self.system_status = "SHUTDOWN"
            logger.info("RK-OS System shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")

def main():
    """Main entry point for RK-OS"""
    print("=" * 60)
    print("RK-OS - Logical Operating System")
    print("Logic 1.0 + 1.1 Implementation")
    print("=" * 60)
    
    # Initialize the system
    rkos = RKOS()
    
    if rkos.system_status == "FAILED":
        print("Failed to initialize RK-OS system!")
        return
    
    try:
        # Demonstrate core functionality
        print("\nDemonstrating Core Logic Operations:")
        print("-" * 40)
        
        # Test basic operations
        operations = [
            ("AND", {"operand1": True, "operand2": False}),
            ("OR", {"operand1": True, "operand2": False}), 
            ("NOT", {"operand": True}),
            ("IMPLIES", {"antecedent": True, "consequent": False}),
            ("BICONDITIONAL", {"operand1": True, "operand2": True})
        ]
        
        for operation, params in operations:
            result = rkos.process_logic_operation(operation, **params)
            if result['success']:
                print(f"{operation}: {result['result']['result']}")
            else:
                print(f"{operation}: ERROR - {result['error']}")
        
        # Test truth table generation
        print("\nGenerating Truth Table:")
        print("-" * 40)
        table_result = rkos.generate_truth_table(['P', 'Q'], "P AND Q")
        if table_result['success']:
            results = table_result['result']['results'][:4]  # Show first few rows
            for row in results:
                vars_str = ', '.join([f"{k}={v}" for k, v in row['variables'].items()])
                print(f"({vars_str}) -> {row['result']}")
        else:
            print("Truth table generation failed!")
        
        # Show system metrics
        print("\nSystem Metrics:")
        print("-" * 40)
        metrics = rkos.get_system_metrics()
        if 'error' not in metrics:
            print(f"Status: {metrics['system_status']}")
            print(f"Uptime: {metrics['uptime_seconds']:.2f} seconds")
        
        print("\nRK-OS System Ready!")
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        rkos.shutdown()

if __name__ == "__main__":
    main()
