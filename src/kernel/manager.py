"""
manager.py - Resource management for RK-OS kernel integration
"""

import time
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ResourceManager:
    """
    System resource manager that handles allocation and deallocation of system resources
    """
    
    def __init__(self):
        """Initialize the resource manager"""
        self.resources = {
            'cpu': {},
            'memory': {},
            'disk': {},
            'network': {}
        }
        
        logger.info("Resource Manager initialized")
        
    def allocate_resource(self, resource_type: str, name: str, **kwargs) -> Dict[str, Any]:
        """
        Allocate a system resource
        
        Args:
            resource_type (str): Type of resource to allocate
            name (str): Resource identifier  
            **kwargs: Additional allocation parameters
            
        Returns:
            dict: Allocation result and metadata
        """
        try:
            logger.info(f"Allocating {resource_type} resource '{name}'")
            
            # Store allocation info
            self.resources[resource_type][name] = {
                'allocated_at': time.time(),
                'parameters': kwargs,
                'status': 'active'
            }
            
            return {
                'success': True,
                'resource_type': resource_type,
                'name': name,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to allocate {resource_type} resource '{name}': {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def deallocate_resource(self, resource_type: str, name: str) -> Dict[str, Any]:
        """
        Deallocate a system resource
        
        Args:
            resource_type (str): Type of resource to deallocate
            name (str): Resource identifier
            
        Returns:
            dict: Deallocation result and metadata
        """
        try:
            logger.info(f"Deallocating {resource_type} resource '{name}'")
            
            if resource_type in self.resources and name in self.resources[resource_type]:
                # Remove from active resources  
                del self.resources[resource_type][name]
                
                return {
                    'success': True,
                    'resource_type': resource_type,
                    'name': name,
                    'timestamp': time.time()
                }
            else:
                logger.warning(f"Resource {name} not found in {resource_type}")
                return {
                    'success': False,
                    'error': f"Resource '{name}' not found",
                    'timestamp': time.time()
                }
                
        except Exception as e:
            logger.error(f"Failed to deallocate {resource_type} resource '{name}': {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def get_resource_status(self, resource_type: str = None) -> Dict[str, Any]:
        """
        Get status of system resources
        
        Args:
            resource_type (str): Specific type to query or None for all
            
        Returns:
            dict: Resource status information
        """
        try:
            if resource_type is not None and resource_type in self.resources:
                return {
                    'success': True,
                    'resource_type': resource_type,
                    'status': self.resources[resource_type],
                    'timestamp': time.time()
                }
            elif resource_type is None:
                # Return status for all resources
                return {
                    'success': True,
                    'resources': self.resources,
                    'timestamp': time.time()
                }
            else:
                return {
                    'success': False,
                    'error': f"Unknown resource type: {resource_type}",
                    'timestamp': time.time()
                }
                
        except Exception as e:
            logger.error(f"Failed to get resource status: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }

# Main instance for system use
resource_manager = ResourceManager()
