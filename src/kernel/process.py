"""
process.py - Process management for RK-OS kernel integration
"""

import psutil
import time
import threading
from typing import Dict, Any, Optional, List
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ProcessManager:
    """
    Manages system processes and process-related operations
    """
    
    def __init__(self):
        """Initialize the process manager"""
        self.active_processes = {}
        self.process_lock = threading.Lock()
        
        logger.info("Process Manager initialized")
        
    def get_process_list(self) -> Dict[str, Any]:
        """
        Get list of all running processes
        
        Returns:
            dict: Process information
        """
        try:
            process_list = []
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
                try:
                    # Get detailed process information
                    pinfo = proc.info
                    
                    # Calculate memory usage in MB
                    mem_mb = round(pinfo['memory_info'].rss / 1024 / 1024, 2) if pinfo['memory_info'] else 0
                    
                    process_list.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'],
                        'username': pinfo['username'],
                        'cpu_percent': round(pinfo['cpu_percent'], 2),
                        'memory_mb': mem_mb,
                        'timestamp': time.time()
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    # Process might have terminated or we don't have access
                    continue
            
            return {
                'success': True,
                'processes': process_list,
                'count': len(process_list),
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to get process list: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def start_process(self, executable: str, args: List[str] = None) -> Dict[str, Any]:
        """
        Start a new system process
        
        Args:
            executable (str): Path to executable
            args (List[str]): Command line arguments
            
        Returns:
            dict: Process start result and metadata
        """
        try:
            logger.info(f"Starting process: {executable}")
            
            # Prepare command with arguments
            cmd = [executable]
            if args:
                cmd.extend(args)
            
            # Start the process (this is a simplified approach)
            # In real implementation, would use subprocess or similar
            pid = 0  # Placeholder - in real system this would be actual PID
            
            return {
                'success': True,
                'executable': executable,
                'args': args,
                'pid': pid,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to start process {executable}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def kill_process(self, pid: int) -> Dict[str, Any]:
        """
        Terminate a running process by PID
        
        Args:
            pid (int): Process ID to terminate
            
        Returns:
            dict: Kill result and metadata
        """
        try:
            if not psutil.pid_exists(pid):
                raise ValueError(f"Process {pid} does not exist")
            
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=5)
            
            logger.info(f"Successfully terminated process {pid}")
            return {
                'success': True,
                'pid': pid,
                'timestamp': time.time(),
                'message': f"Process {pid} terminated successfully"
            }
            
        except psutil.TimeoutExpired:
            # Force kill if normal termination fails
            try:
                proc = psutil.Process(pid)
                proc.kill()
                logger.info(f"Force killed process {pid}")
                return {
                    'success': True,
                    'pid': pid,
                    'timestamp': time.time(),
                    'message': f"Process {pid} force killed"
                }
            except Exception as e:
                logger.error(f"Failed to kill process {pid}: {str(e)}")
                return {
                    'success': False,
                    'error': str(e),
                    'timestamp': time.time()
                }
        except Exception as e:
            logger.error(f"Failed to kill process {pid}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def get_process_info(self, pid: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific process
        
        Args:
            pid (int): Process ID
            
        Returns:
            dict: Process details
        """
        try:
            if not psutil.pid_exists(pid):
                return {
                    'success': False,
                    'error': f"Process {pid} does not exist",
                    'timestamp': time.time()
                }
            
            proc = psutil.Process(pid)
            
            # Get process information  
            info = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 
                                     'memory_info', 'create_time', 'status'])
            
            # Calculate memory usage in MB
            mem_mb = round(info['memory_info'].rss / 1024 / 1024, 2) if info['memory_info'] else 0
            
            return {
                'success': True,
                'pid': pid,
                'name': info['name'],
                'username': info['username'],
                'cpu_percent': round(info['cpu_percent'], 2),
                'memory_mb': mem_mb,
                'create_time': info['create_time'],
                'status': info['status'],
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to get process info for PID {pid}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }

# Main instance for system use
process_manager = ProcessManager()
