"""
binary_serializer.py - Binary serialization for RK-OS performance optimization
"""

import pickle
import time
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class BinarySerializer:
    """
    Binary serializer that provides high-performance data serialization
    """
    
    def __init__(self):
        """Initialize the binary serializer"""
        logger.info("Binary Serializer initialized")
        
    def serialize(self, data: Dict[str, Any]) -> bytes:
        """
        Serialize data to binary format
        
        Args:
            data (Dict): Data to serialize
            
        Returns:
            bytes: Serialized binary data
        """
        try:
            serialized_data = pickle.dumps(data)
            logger.info(f"Binary serialization completed ({len(serialized_data)} bytes)")
            return serialized_data
            
        except Exception as e:
            logger.error(f"Failed to serialize data to binary: {str(e)}")
            raise
    
    def deserialize(self, binary_data: bytes) -> Dict[str, Any]:
        """
        Deserialize binary data back to dictionary format
        
        Args:
            binary_data (bytes): Binary serialized data
            
        Returns:
            dict: Deserialized data
        """
        try:
            deserialized_data = pickle.loads(binary_data)
            logger.info("Binary deserialization completed")
            return deserialized_data
            
        except Exception as e:
            logger.error(f"Failed to deserialize binary data: {str(e)}")
            raise
    
    def save_to_file(self, data: Dict[str, Any], filename: str) -> bool:
        """
        Save serialized binary data to a file
        
        Args:
            data (Dict): Data to save
            filename (str): Output file name
            
        Returns:
            bool: True if successful
        """
        try:
            # Serialize the data
            binary_data = self.serialize(data)
            
            # Save to file in binary mode
            with open(filename, 'wb') as f:
                f.write(binary_data)
                
            logger.info(f"Binary data saved successfully to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save binary data to file '{filename}': {str(e)}")
            return False
    
    def load_from_file(self, filename: str) -> Dict[str, Any]:
        """
        Load and deserialize binary data from a file
        
        Args:
            filename (str): Input file name
            
        Returns:
            dict: Loaded and deserialized data
        """
        try:
            with open(filename, 'rb') as f:
                binary_data = f.read()
            
            # Deserialize the data
            data = self.deserialize(binary_data)
            
            logger.info(f"Binary data loaded successfully from {filename}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load binary data from file '{filename}': {str(e)}")
            raise

# Main instance for system use
binary_serializer = BinarySerializer()

# Example usage  
if __name__ == "__main__":
    # Test binary serialization
    test_data = {
        'system_info': {
            'name': 'RK-OS',
            'version': '1.0.0', 
            'status': 'running'
        },
        'metrics': [45.2, 67.8, 32.1, 89.5],
        'config': {'debug': True, 'log_level': 'INFO'}
    }
    
    # Serialize and save to file
    serializer = BinarySerializer()
    
    if serializer.save_to_file(test_data, "test_binary_state.bin"):
        print("Binary data saved successfully")
        
        # Load data back  
        loaded_data = serializer.load_from_file("test_binary_state.bin")
        print(f"Loaded binary data: {loaded_data}")
