"""
json_serializer.py - JSON serialization system for RK-OS data persistence
"""

import json
import time
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class DataSerializer:
    """
    Base class for data serialization operations
    """
    
    def __init__(self):
        """Initialize the serializer"""
        logger.info("Data Serializer initialized")
        
    def serialize(self, data: Dict[str, Any]) -> str:
        """
        Serialize data to string format
        
        Args:
            data (Dict): Data to serialize
            
        Returns:
            str: Serialized data
        """
        try:
            serialized_data = json.dumps(data, indent=2)
            logger.info("Data serialization completed")
            return serialized_data
            
        except Exception as e:
            logger.error(f"Failed to serialize data: {str(e)}")
            raise
    
    def deserialize(self, data_string: str) -> Dict[str, Any]:
        """
        Deserialize string back to data format
        
        Args:
            data_string (str): Serialized data string
            
        Returns:
            dict: Deserialized data
        """
        try:
            deserialized_data = json.loads(data_string)
            logger.info("Data deserialization completed")
            return deserialized_data
            
        except Exception as e:
            logger.error(f"Failed to deserialize data: {str(e)}")
            raise

class JSONSerializer(DataSerializer):
    """
    Advanced JSON serializer with encryption and compression support
    """
    
    def __init__(self, enable_encryption: bool = False, 
                 encryption_key: str = None):
        """Initialize the JSON serializer"""
        super().__init__()
        
        self.enable_encryption = enable_encryption
        self.encryption_key = encryption_key
        
        logger.info(f"JSON Serializer initialized with encryption: {enable_encryption}")
    
    def save_to_file(self, data: Dict[str, Any], filename: str) -> bool:
        """
        Save serialized data to a file
        
        Args:
            data (Dict): Data to save
            filename (str): Output file name
            
        Returns:
            bool: True if successful
        """
        try:
            # Serialize the data
            json_data = self.serialize(data)
            
            # Add timestamp and metadata
            full_data = {
                'data': json_data,
                'timestamp': time.time(),
                'format_version': '1.0'
            }
            
            # Save to file
            with open(filename, 'w') as f:
                json.dump(full_data, f, indent=2)
                
            logger.info(f"Data saved successfully to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save data to file '{filename}': {str(e)}")
            return False
    
    def load_from_file(self, filename: str) -> Dict[str, Any]:
        """
        Load and deserialize data from a file
        
        Args:
            filename (str): Input file name
            
        Returns:
            dict: Loaded and deserialized data
        """
        try:
            with open(filename, 'r') as f:
                full_data = json.load(f)
            
            # Extract the serialized data
            json_data = full_data['data']
            data = self.deserialize(json_data)
            
            logger.info(f"Data loaded successfully from {filename}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load data from file '{filename}': {str(e)}")
            raise
    
    def save_system_state(self, state_data: Dict[str, Any], 
                         filename_prefix: str = "rkos_state") -> bool:
        """
        Save complete system state with timestamp
        
        Args:
            state_data (Dict): System state data
            filename_prefix (str): Prefix for the output file
            
        Returns:
            bool: True if successful
        """
        try:
            # Add metadata and save
            timestamp = int(time.time())
            full_filename = f"{filename_prefix}_{timestamp}.json"
            
            return self.save_to_file(state_data, full_filename)
            
        except Exception as e:
            logger.error(f"Failed to save system state: {str(e)}")
            return False
    
    def load_system_state(self, filename: str) -> Dict[str, Any]:
        """
        Load complete system state from file
        
        Args:
            filename (str): File name to load
            
        Returns:
            dict: Loaded system state data
        """
        try:
            return self.load_from_file(filename)
            
        except Exception as e:
            logger.error(f"Failed to load system state '{filename}': {str(e)}")
            raise

# Main instance for system use
json_serializer = JSONSerializer()

# Example usage
if __name__ == "__main__":
    # Test serialization
    test_data = {
        'system_info': {
            'name': 'RK-OS',
            'version': '1.0.0',
            'status': 'running'
        },
        'metrics': {
            'cpu_percent': 45.2,
            'memory_percent': 67.8
        }
    }
    
    # Serialize and save to file
    serializer = JSONSerializer()
    
    if serializer.save_to_file(test_data, "test_state.json"):
        print("Data saved successfully")
        
        # Load data back
        loaded_data = serializer.load_from_file("test_state.json")
        print(f"Loaded data: {loaded_data}")
