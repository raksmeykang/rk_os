"""
scheduler.py - Task scheduling and management for RK-OS
"""

import time
import threading
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TaskScheduler:
    """
    System task scheduler for managing concurrent logical operations
    """
    
    def __init__(self):
        """Initialize the task scheduler"""
        self.tasks = {}
        self.active_tasks = {}
        self.task_counter = 0
        
        # Threading support
        self._lock = threading.Lock()
        
        logger.info("Task Scheduler initialized")
        
    def schedule_task(self, name: str, function: Callable, 
                     args: tuple = (), kwargs: dict = None, 
                     interval: float = 0.0) -> str:
        """
        Schedule a task for execution
        
        Args:
            name (str): Task name
            function (Callable): Function to execute  
            args (tuple): Arguments for the function
            kwargs (dict): Keyword arguments for the function
            interval (float): Execution interval in seconds (0 = one-time)
            
        Returns:
            str: Task ID
        """
        with self._lock:
            task_id = f"task_{self.task_counter}"
            self.task_counter += 1
            
            # Store task information
            self.tasks[task_id] = {
                'name': name,
                'function': function,
                'args': args,
                'kwargs': kwargs or {},
                'interval': interval,
                'created_at': datetime.now(),
                'status': 'scheduled'
            }
            
            logger.info(f"Task '{name}' scheduled with ID: {task_id}")
            return task_id
    
    def start_task(self, task_id: str) -> bool:
        """Start a scheduled task"""
        try:
            if task_id not in self.tasks:
                raise ValueError(f"Task {task_id} not found")
                
            task = self.tasks[task_id]
            
            # Mark as started
            task['status'] = 'running'
            task['started_at'] = datetime.now()
            
            logger.info(f"Task '{task['name']}' started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start task {task_id}: {str(e)}")
            return False
    
    def stop_task(self, task_id: str) -> bool:
        """Stop a running task"""
        try:
            if task_id not in self.tasks:
                raise ValueError(f"Task {task_id} not found")
                
            task = self.tasks[task_id]
            task['status'] = 'stopped'
            
            logger.info(f"Task '{task['name']}' stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop task {task_id}: {str(e)}")
            return False
    
    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute a scheduled task immediately"""
        try:
            if task_id not in self.tasks:
                raise ValueError(f"Task {task_id} not found")
            
            task = self.tasks[task_id]
            start_time = time.time()
            
            # Execute the function
            result = task['function'](*task['args'], **task['kwargs'])
            
            execution_time = time.time() - start_time
            
            logger.info(f"Task '{task['name']}' executed successfully in {execution_time:.4f}s")
            
            return {
                'success': True,
                'task_id': task_id,
                'result': result,
                'execution_time': execution_time
            }
            
        except Exception as e:
            logger.error(f"Failed to execute task {task_id}: {str(e)}")
            return {
                'success': False,
                'task_id': task_id,
                'error': str(e)
            }
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of a specific task"""
        try:
            if task_id not in self.tasks:
                raise ValueError(f"Task {task_id} not found")
                
            return {
                'success': True,
                'task_info': self.tasks[task_id]
            }
        except Exception as e:
            logger.error(f"Failed to get task status for {task_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_tasks(self) -> Dict[str, Any]:
        """List all scheduled tasks"""
        try:
            task_list = []
            for task_id, task_info in self.tasks.items():
                task_list.append({
                    'id': task_id,
                    'name': task_info['name'],
                    'status': task_info['status']
                })
                
            return {
                'success': True,
                'tasks': task_list
            }
        except Exception as e:
            logger.error(f"Failed to list tasks: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

# Global scheduler instance
scheduler = TaskScheduler()
