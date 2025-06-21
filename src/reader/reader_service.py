from .base import Reader

class ReaderService:
  """
  A service class to handle RFID reader operations.

  This class provides functionality to interact with an RFID reader device, 
  including reading tags and handling GPIO cleanup on Raspberry Pi.

  Attributes:
    reader: The RFID reader device instance.
    gpio: GPIO controller instance, used for Raspberry Pi.
  """
  def __init__(
      self,
      reader: Reader = None,
    ):
    self.reader = reader

  def read(self):
    """
    Reads data from the RFID reader.

    This method attempts to read the RFID tag's ID and text content.
    If successful, it returns the ID and text.
    On Raspberry Pi devices, GPIO cleanup is performed in the finally block
    to ensure proper resource management regardless of success or failure.

    Returns:
      tuple: A tuple containing the ID and text read from the RFID tag. Returns none if no tag is detected or if an error occurs.
    """
    try:
      id, text = self.reader.read()
      return id, text
    except Exception as e:
      return None, None
    finally:
      self.reader.cleanup()