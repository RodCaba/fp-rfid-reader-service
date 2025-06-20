from ..base import Reader
from mfrc522 import MFRC522
import RPi.GPIO as GPIO
from time import sleep

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
      tuple: A tuple containing (id, text) from the RFID tag

    Raises:
      Exception: If there's an error reading the tag
    """
    try:
      status, _ = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
      if status != self.reader.MI_OK:
        sleep(0.1)
        return
      status, back_data = self.reader.MFRC522_Anticoll()
      buf = self.reader.MFRC522_Read(0)
      self.reader.MFRC522_Request(self.reader.PICC_HALT)
      if buf:
        print([hex(x) for x in buf])
    except Exception as e:
      print(e)
      
  def cleanup(self):
    """
    Clean up GPIO resources
    """
    GPIO.cleanup()