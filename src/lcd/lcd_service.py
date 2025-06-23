from .base import Writer

class LCDService:
  """
  A service class for managing LCD operations.

  Attributes:
    writer: An instance of a Writer class that handles LCD writing operations.
  """
  def __init__(self, writer: Writer):
    """
    Initializes the LCDService with a specific Writer instance.

    Args:
      writer (Writer): An instance of a Writer class that implements the LCD writing functionality.
    """
    self.writer = writer

  def write(self, text: str):
    """
    Writes text to the LCD display.

    Args:
      text (str): The text to be displayed on the LCD.
    """
    try:
      self.writer.write(text)
    except Exception as e:
      print(f"Error writing to LCD: {e}")

  def clear(self):
    """
    Clears the LCD display.
    
    This method calls the clear method of the Writer instance to clear any text currently displayed.
    """
    try:
      self.writer.clear()
    except Exception as e:
      print(f"Error clearing LCD: {e}")
