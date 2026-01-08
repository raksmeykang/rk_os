"""
xml_serializer.py - XML serialization for RK-OS compatibility and interchange
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import time
from typing import Dict, Any, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class XMLSerializer:
    """
    XML serializer that provides structured data interchange format
    """
    
    def __init__(self):
        """Initialize the XML serializer"""
        logger.info("XML Serializer initialized")
        
    def dict_to_xml(self, data: Dict[str, Any], root_name: str = "data") -> str:
        """
        Convert dictionary to XML string
        
        Args:
            data (Dict): Data to convert
            root_name (str): Root element name
            
        Returns:
            str: XML representation as string
        """
        try:
            # Create root element
            root = ET.Element(root_name)
            
            # Recursively add elements
            self._dict_to_xml_element(data, root)
            
            # Pretty print the XML
            rough_string = ET.tostring(root, encoding='unicode')
            reparsed = minidom.parseString(rough_string)
            pretty_xml = reparsed.toprettyxml(indent="  ")
            
            logger.info(f"XML conversion completed")
            return pretty_xml
            
        except Exception as e:
            logger.error(f"Failed to convert dictionary to XML: {str(e)}")
            raise
    
    def _dict_to_xml_element(self, data: Dict[str, Any], parent: ET.Element):
        """
        Recursively add dictionary elements to XML
        
        Args:
            data (Dict): Dictionary data
            parent (ET.Element): Parent XML element
        """
        try:
            for key, value in data.items():
                # Sanitize the key name (remove invalid characters)
                safe_key = self._sanitize_xml_tag(key)
                
                if isinstance(value, dict):
                    # Create sub-element for nested dictionary
                    child = ET.SubElement(parent, safe_key)
                    self._dict_to_xml_element(value, child)
                elif isinstance(value, list):
                    # Handle lists by creating multiple elements
                    for item in value:
                        item_element = ET.SubElement(parent, f"{safe_key}_item")
                        if isinstance(item, dict):
                            self._dict_to_xml_element(item, item_element)
                        else:
                            item_element.text = str(item)
                else:
                    # Create simple element with text content
                    child = ET.SubElement(parent, safe_key)
                    child.text = str(value)
                    
        except Exception as e:
            logger.error(f"Failed to add XML elements: {str(e)}")
            raise
    
    def _sanitize_xml_tag(self, tag_name: str) -> str:
        """
        Sanitize a string for use as an XML tag name
        
        Args:
            tag_name (str): Original tag name
            
        Returns:
            str: Sanitized tag name
        """
        try:
            # Replace invalid characters with underscores
            sanitized = ''.join(c if c.isalnum() or c in ['_', '-', '.'] else '_' for c in tag_name)
            
            # Ensure it doesn't start with a number
            if sanitized and sanitized[0].isdigit():
                sanitized = f"_{sanitized}"
                
            return sanitized
            
        except Exception as e:
            logger.error(f"Failed to sanitize XML tag '{tag_name}': {str(e)}")
            return "invalid_tag"
    
    def xml_to_dict(self, xml_string: str) -> Dict[str, Any]:
        """
        Convert XML string back to dictionary
        
        Args:
            xml_string (str): XML string
            
        Returns:
            dict: Converted data
        """
        try:
            root = ET.fromstring(xml_string)
            return self._xml_element_to_dict(root)
            
        except Exception as e:
            logger.error(f"Failed to convert XML to dictionary: {str(e)}")
            raise
    
    def _xml_element_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """
        Recursively convert XML elements to dictionary
        
        Args:
            element (ET.Element): XML element
            
        Returns:
            dict: Converted data
        """
        try:
            result = {}
            
            # Process child elements
            for child in element:
                if len(child) == 0:
                    # Simple text content
                    result[child.tag] = child.text
                else:
                    # Nested elements - recurse
                    nested_data = self._xml_element_to_dict(child)
                    
                    # Handle lists of same-type items  
                    if child.tag in result:
                        if not isinstance(result[child.tag], list):
                            result[child.tag] = [result[child.tag]]
                        result[child.tag].append(nested_data)
                    else:
                        result[child.tag] = nested_data
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to convert XML element to dictionary: {str(e)}")
            raise
    
    def save_to_file(self, data: Dict[str, Any], filename: str) -> bool:
        """
        Save serialized XML data to a file
        
        Args:
            data (Dict): Data to save
            filename (str): Output file name
            
        Returns:
            bool: True if successful
        """
        try:
            # Convert dictionary to XML
            xml_string = self.dict_to_xml(data)
            
            # Add metadata and save to file
            with open(filename, 'w') as f:
                f.write(xml_string)
                
            logger.info(f"XML data saved successfully to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save XML data to file '{filename}': {str(e)}")
            return False
    
    def load_from_file(self, filename: str) -> Dict[str, Any]:
        """
        Load and deserialize XML data from a file
        
        Args:
            filename (str): Input file name
            
        Returns:
            dict: Loaded and deserialized data
        """
        try:
            with open(filename, 'r') as f:
                xml_string = f.read()
            
            # Deserialize the XML back to dictionary
            data = self.xml_to_dict(xml_string)
            
            logger.info(f"XML data loaded successfully from {filename}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load XML data from file '{filename}': {str(e)}")
            raise

# Main instance for system use
xml_serializer = XMLSerializer()

# Example usage
if __name__ == "__main__":
    # Test XML serialization  
    test_data = {
        'system_info': {
            'name': 'RK-OS',
            'version': '1.0.0',
            'status': 'running'
        },
        'metrics': [45.2, 67.8, 32.1, 89.5],
        'config': {
            'debug': True,
            'log_level': 'INFO',
            'features': ['security', 'monitoring']
        }
    }
    
    # Serialize and save to file
    serializer = XMLSerializer()
    
    if serializer.save_to_file(test_data, "test_xml_state.xml"):
        print("XML data saved successfully")
        
        # Load data back
        loaded_data = serializer.load_from_file("test_xml_state.xml")
        print(f"Loaded XML data: {loaded_data}")
