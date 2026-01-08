"""
kernel_bridge.py - OS Kernel Integration Layer for RK-OS
"""

import os
import sys
import platform
import psutil
import threading
import time
from typing import Dict, Any, Optional, List
import logging

# Configure logging
logger = logging.getLogger(__name__)

class KernelBridge:
    """
    Bridge between RK-OS logic system and the underlying operating system kernel.
    Provides integration with OS resources and process management.
    """
    
    def __init__(self):
        """Initialize kernel bridge"""
        self.system_info = {}
        self.resource_usage = {}
        self.processes = []
        self.is_initialized = False
        
        logger.info("Kernel Bridge initialized")
        self._initialize_system_info()
        
    def _initialize_system_info(self):
        """Collect basic system information"""
        try:
            self.system_info = {
                'platform': platform.platform(),
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'architecture': platform.architecture()[0],
                'python_version': sys.version,
                'os_name': os.name
            }
            
            # Collect memory information
            memory = psutil.virtual_memory()
            self.system_info['memory_total'] = memory.total
            self.system_info['memory_available'] = memory.available
            self.system_info['memory_percent'] = memory.percent
            
            self.is_initialized = True
            logger.info(f"System info collected: {self.system_info}")
            
        except Exception as e:
            logger.error(f"Failed to initialize system info: {str(e)}")
    
    def get_system_resources(self) -> Dict[str, Any]:
        """Get current system resource usage"""
        try:
            if not self.is_initialized:
                return {}
                
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage  
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Network connections
            net_connections = len(psutil.net_connections())
            
            self.resource_usage = {
                'cpu_percent': cpu_percent,
                'memory_total': memory.total,
                'memory_available': memory.available,
                'memory_used': memory.used,
                'memory_percent': memory.percent,
                'disk_total': disk.total,
                'disk_used': disk.used,
                'disk_free': disk.free,
                'disk_percent': disk.percent,
                'network_connections': net_connections,
                'timestamp': time.time()
            }
            
            return self.resource_usage
            
        except Exception as e:
            logger.error(f"Failed to get system resources: {str(e)}")
            return {}
    
    def execute_system_call(self, call_type: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute OS-level system calls
        
        Args:
            call_type (str): Type of system call
            parameters (Dict): Parameters for the system call
            
        Returns:
            Dict with result and metadata
        """
        try:
            logger.info(f"Executing system call: {call_type}")
            
            if not parameters:
                parameters = {}
                
            # Handle different types of system calls
            if call_type == "get_process_list":
                return self._get_processes()
            elif call_type == "kill_process":
                return self._kill_process(parameters.get('pid'))
            elif call_type == "get_disk_usage":
                return self._get_disk_usage()
            elif call_type == "get_network_info":
                return self._get_network_info()
            elif call_type == "execute_command":
                return self._execute_shell_command(parameters.get('command', ''))
            else:
                logger.warning(f"Unknown system call type: {call_type}")
                raise ValueError(f"Unknown system call: {call_type}")
                
        except Exception as e:
            logger.error(f"System call failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def _get_processes(self) -> Dict[str, Any]:
        """Get list of running processes"""
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
            
            self.processes = process_list
            return {
                'success': True,
                'processes': process_list,
                'count': len(process_list),
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to get processes: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def _kill_process(self, pid: int) -> Dict[str, Any]:
        """Kill a process by PID"""
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
    
    def _get_disk_usage(self) -> Dict[str, Any]:
        """Get disk usage information"""
        try:
            # Get root partition usage
            disk = psutil.disk_usage('/')
            
            return {
                'success': True,
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent,
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Failed to get disk usage: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def _get_network_info(self) -> Dict[str, Any]:
        """Get network connection information"""
        try:
            connections = psutil.net_connections(kind='inet')
            
            # Count by type
            tcp_count = sum(1 for c in connections if c.type == socket.SOCK_STREAM)
            udp_count = sum(1 for c in connections if c.type == socket.SOCK_DGRAM)
            
            return {
                'success': True,
                'total_connections': len(connections),
                'tcp_connections': tcp_count,
                'udp_connections': udp_count,
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Failed to get network info: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def _execute_shell_command(self, command: str) -> Dict[str, Any]:
        """Execute a shell command"""
        try:
            import subprocess
            
            # Execute the command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            return {
                'success': True,
                'command': command,
                'returncode': result.returncode,
                'stdout': result.stdout.strip(),
                'stderr': result.stderr.strip(),
                'timestamp': time.time()
            }
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {command}")
            return {
                'success': False,
                'error': "Command execution timeout",
                'command': command,
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Failed to execute command '{command}': {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'command': command,
                'timestamp': time.time()
            }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get complete system information"""
        try:
            # Update resource usage
            self.get_system_resources()
            
            return {
                'success': True,
                'system_info': self.system_info,
                'resource_usage': self.resource_usage,
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Failed to get system info: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def manage_resources(self, resource_type: str, action: str, **kwargs) -> Dict[str, Any]:
        """
        Manage system resources
        
        Args:
            resource_type (str): Type of resource to manage
            action (str): Action to perform
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with result and metadata
        """
        try:
            logger.info(f"Managing {resource_type} - Action: {action}")
            
            if resource_type == "memory":
                return self._manage_memory(action, kwargs)
            elif resource_type == "cpu":
                return self._manage_cpu(action, kwargs)
            else:
                raise ValueError(f"Unknown resource type: {resource_type}")
                
        except Exception as e:
            logger.error(f"Resource management failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def _manage_memory(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Manage memory resources"""
        try:
            if action == "get_info":
                return {
                    'success': True,
                    'memory_info': self.get_system_resources(),
                    'timestamp': time.time()
                }
            elif action == "optimize":
                # In a real implementation this would perform memory optimization
                logger.info("Memory optimization requested")
                return {
                    'success': True,
                    'action': 'optimized',
                    'timestamp': time.time()
                }
            else:
                raise ValueError(f"Unknown memory management action: {action}")
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def _manage_cpu(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Manage CPU resources"""
        try:
            if action == "get_info":
                return {
                    'success': True,
                    'cpu_info': psutil.cpu_percent(interval=1),
                    'timestamp': time.time()
                }
            elif action == "set_priority":
                # In a real implementation this would set process priorities
                logger.info("CPU priority management requested")
                return {
                    'success': True,
                    'action': 'priority_set',
                    'timestamp': time.time()
                }
            else:
                raise ValueError(f"Unknown CPU management action: {action}")
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }

# For testing purposes
if __name__ == "__main__":
    # Initialize the kernel bridge
    kernel_bridge = KernelBridge()
    
    print("Kernel Bridge Test")
    print("=" * 30)
    
    # Get system information
    info = kernel_bridge.get_system_info()
    if info['success']:
        print(f"System: {info['system_info']['platform']}")
        print(f"CPU Usage: {info['resource_usage']['cpu_percent']}%")
        print(f"Memory Available: {info['resource_usage']['memory_available'] / (1024**3):.2f} GB")
    
    # Get process list
    processes = kernel_bridge.execute_system_call("get_process_list")
    if processes['success']:
        print(f"\nFound {processes['count']} running processes")
