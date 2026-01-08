"""
encryption.py - Data encryption utilities for RK-OS security framework
"""

import hashlib
import secrets
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class DataEncryption:
    """
    Advanced data encryption and decryption system for RK-OS
    """
    
    def __init__(self):
        """Initialize the encryption manager"""
        self.encryption_keys = {}
        
        logger.info("Data Encryption Manager initialized")
        
    def generate_encryption_key(self, key_length: int = 32) -> str:
        """
        Generate a secure random encryption key
        
        Args:
            key_length (int): Length of the key in bytes
            
        Returns:
            str: Generated encryption key
        """
        try:
            # Generate a cryptographically secure random key
            key = secrets.token_bytes(key_length)
            key_hex = key.hex()
            
            logger.info(f"Generated {key_length}-byte encryption key")
            return key_hex
            
        except Exception as e:
            logger.error(f"Failed to generate encryption key: {str(e)}")
            raise
    
    def encrypt_data(self, data: str, key: str) -> Dict[str, Any]:
        """
        Encrypt data using a given key
        
        Args:
            data (str): Data to encrypt
            key (str): Encryption key
            
        Returns:
            dict: Encrypted data and metadata
        """
        try:
            # Simple XOR encryption for demonstration purposes
            # In production, use proper cryptographic libraries like cryptography or PyCryptodome
            encrypted_bytes = bytearray()
            
            key_bytes = bytes.fromhex(key)
            data_bytes = data.encode('utf-8')
            
            # XOR each byte with corresponding key byte (cycling through the key)
            for i, byte in enumerate(data_bytes):
                key_byte = key_bytes[i % len(key_bytes)]
                encrypted_bytes.append(byte ^ key_byte)
            
            encrypted_data = encrypted_bytes.hex()
            
            return {
                'success': True,
                'data': encrypted_data,
                'algorithm': 'XOR',
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to encrypt data: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def decrypt_data(self, encrypted_data: str, key: str) -> Dict[str, Any]:
        """
        Decrypt data using a given key
        
        Args:
            encrypted_data (str): Encrypted data to decrypt
            key (str): Decryption key
            
        Returns:
            dict: Decrypted data and metadata  
        """
        try:
            # XOR decryption is the same as encryption for XOR cipher
            encrypted_bytes = bytes.fromhex(encrypted_data)
            key_bytes = bytes.fromhex(key)
            
            decrypted_bytes = bytearray()
            
            # XOR each byte with corresponding key byte (cycling through the key)
            for i, byte in enumerate(encrypted_bytes):
                key_byte = key_bytes[i % len(key_bytes)]
                decrypted_bytes.append(byte ^ key_byte)
            
            decrypted_data = decrypted_bytes.decode('utf-8')
            
            return {
                'success': True,
                'data': decrypted_data,
                'algorithm': 'XOR',
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to decrypt data: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def hash_data(self, data: str, algorithm: str = "sha256") -> Dict[str, Any]:
        """
        Hash data using specified algorithm
        
        Args:
            data (str): Data to hash
            algorithm (str): Hashing algorithm
            
        Returns:
            dict: Hashed data and metadata
        """
        try:
            # Supported algorithms
            supported_algorithms = {
                'sha256': hashlib.sha256,
                'sha1': hashlib.sha1,
                'md5': hashlib.md5
            }
            
            if algorithm not in supported_algorithms:
                raise ValueError(f"Unsupported hash algorithm: {algorithm}")
            
            # Hash the data
            hasher = supported_algorithms[algorithm]()
            hasher.update(data.encode('utf-8'))
            hashed_data = hasher.hexdigest()
            
            return {
                'success': True,
                'data': hashed_data,
                'algorithm': algorithm,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to hash data: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }

# Main instance for system use
data_encryption = DataEncryption()
