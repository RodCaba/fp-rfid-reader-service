from abc import ABC, abstractmethod

class Reader(ABC):
    """
    Abstract base class for RFID readers.
    
    This class defines the interface that all concrete RFID reader 
    implementations must follow.
    """
    
    @abstractmethod
    def read(self):
        """
        Read data from an RFID tag.
        
        Returns:
            tuple: A tuple containing (id, text) from the RFID tag
            
        Raises:
            Exception: If there's an error reading the tag
        """
        pass
    
    @abstractmethod
    def cleanup(self):
        """
        Clean up resources used by the reader.
        
        This method should be called when the reader is no longer needed
        to free up any system resources.
        """
        pass