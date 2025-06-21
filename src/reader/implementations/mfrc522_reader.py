from ..base import Reader
from mfrc522 import MFRC522
import RPi.GPIO as GPIO

class MFRC522Reader(Reader):
  """
  Concrete implementation of the reader interface for MFRC522 RFID readers.
  """
  def __init__(self):
    self.reader = MFRC522()

  def read(self):
    """
    Read data from an RFID tag using the MFRC522 reader

    Returns:
      tuple: A tuple containing (id, text) from the RFID tag.

    Raises:
      Exception: If there's an error reading the tag
    """
    (status, tagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
    if status == self.reader.MI_OK:
      (status, uid) = self.reader.MFRC522_Anticoll()

      if status == self.reader.MI_OK:
        return uid, "Sample Text"
      else:
        raise Exception("Failed to read UID from tag")
  
    else:
      raise Exception("No tag detected")
    
  def cleanup(self):
    pass