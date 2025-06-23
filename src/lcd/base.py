from abc import ABC, abstractmethod

class Writer(ABC):
    """
    Abstract base class for LCD writers.
    
    This class defines the interface that all concrete LCD writer 
    implementations must follow.
    """
    def __init__(
            self,
            i2c_expander="PCF8574",
            address=0x27,
            port=1,
            cols=16,
            rows=2,
            dotsize=8,
        ):
        """
        Initialize the LCD writer.
        
        This method can be overridden by subclasses to perform any necessary
        setup for the LCD display.
        """
        self.i2c_expander = i2c_expander
        self.address = address
        self.port = port
        self.cols = cols
        self.rows = rows
        self.dotsize = dotsize

    def __del__(self):
        """
        Clean up resources when the LCD writer is deleted.
        
        The LCD display should be cleared to ensure no residual text
        remains when the writer is no longer in use.
        """
        try:
            self.clear()
        except Exception as e:
            print(f"Error during cleanup: {e}")

    @abstractmethod
    def write(self, text: str):
        """
        Write text to the LCD display.
        
        Args:
            text (str): The text to display on the LCD.
            
        Raises:
            Exception: If there's an error writing to the display.
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Clear the LCD display.
        
        This method should be called to clear any text currently displayed
        on the LCD.
        Raises:
            Exception: If there's an error clearing the display.
        """
        pass