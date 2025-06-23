from src.reader.reader_service import ReaderService
from src.reader.implementations.mfrc522_reader import MFRC522Reader

from src.lcd.lcd_service import LCDService
from src.lcd.implementations.charlcd_writer import CharLCDWriter

from src.led.led_service import LedService
from RPi import GPIO
from time import sleep

RED_LED_PIN = 5
IS_READING = False

def main():
  red_led = LedService(GPIO, RED_LED_PIN)
  red_led.turn_on()

  lcd_writer = CharLCDWriter(
    i2c_expander='PCF8574',
    address=0x27,
  )
  lcd_service = LCDService(lcd_writer)
  lcd_service.write("Starting RFID Reader...")
  while True:
    try:
      run_reader_service()
    except KeyboardInterrupt:
      print("Exiting...")
      break
    except Exception as e:
      print(f"An error occurred: {e}")
  GPIO.cleanup()  # Clean up GPIO settings on exit

def run_reader_service():
  reader = MFRC522Reader()
  reader_service = ReaderService(
    reader=reader,
  )
  id, text = reader_service.read()
  if id is not None:
    print(f"ID: {id}, Text: {text}")
  else:
    sleep(0.1)  # Wait before retrying if no tag is detected

if __name__ == "__main__":
  main()