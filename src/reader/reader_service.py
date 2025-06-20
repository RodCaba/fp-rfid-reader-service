class ReaderService:
  """
  A service class to handle RFID reader operations.

  This class provides functionality to interact with an RFID reader device, 
  including reading tags and handling GPIO cleanup on Raspberry Pi.

  Attributes:
    reader: The RFID reader device instance.
    gpio: GPIO controller instance, used for Raspberry Pi.
    is_raspberry_pi (bool): Flag indicating if the code is running on a Raspberry Pi.
  """
  def __init__(
      self,
      reader = None,
      gpio = None,
      is_raspberry_pi: bool = False,
    ):
    self.reader = reader
    self.gpio = gpio
    self.is_raspberry_pi = is_raspberry_pi

  def read(self):
    """
    Reads data from the RFID reader.

    This method attempts to read the RFID tag's ID and text content.
    If successful, it returns the ID and text.
    On Raspberry Pi devices, GPIO cleanup is performed in the finally block
    to ensure proper resource management regardless of success or failure.

    Returns:
      tuple: A tuple containing the ID and text read from the RFID tag.

    Raises:
      Any exceptions raised by the reader's read method are propagated to the caller.
    """
    try:
      id, text = self.reader.read()
      return id, text
    finally:
      if self.is_raspberry_pi:
        if self.gpio:
          self.gpio.cleanup()