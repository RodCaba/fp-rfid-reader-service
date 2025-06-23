from src.reader.reader_service import ReaderService
from src.reader.implementations.mfrc522_reader import MFRC522Reader

from src.lcd.lcd_service import LCDService
from src.lcd.implementations.charlcd_writer import CharLCDWriter

from src.gpio.gpio_controller import GPIOController
from RPi import GPIO
from time import sleep

RED_LED_PIN = 5
GREEN_LED_PIN = 6
BUZZER_PIN = 16
IS_READING = False

def main():
  red_led = GPIOController(GPIO, RED_LED_PIN)
  red_led.turn_on()

  green_led = GPIOController(GPIO, GREEN_LED_PIN)
  green_led.turn_off()

  buzzer = GPIOController(GPIO, BUZZER_PIN, component_type="BUZZER")

  lcd_writer = CharLCDWriter(
    i2c_expander='PCF8574',
    address=0x27,
  )
  lcd_service = LCDService(lcd_writer)
  lcd_service.write("RFID Reader started")

  reader = MFRC522Reader()
  reader_service = ReaderService(
    reader=reader,
  )
  while True:
    try:
      id, text = reader_service.read()
      global IS_READING
      if id is not None:
        lcd_service.clear()
        buzzer.turn_on()
        sleep(0.5)  # Buzzer on for 0.5 seconds
        buzzer.turn_off()
        if not IS_READING:
          lcd_service.write("Welcome!")
          IS_READING = True
          red_led.turn_off()
          green_led.turn_on()
        else:
          lcd_service.write("Goodbye!")
          IS_READING = False
          red_led.turn_on()
          green_led.turn_off()
        sleep(3)
        lcd_service.clear()
      else:
        sleep(0.1)  # Wait before retrying if no tag is detected
    except KeyboardInterrupt:
      print("Exiting...")
      break
    except Exception as e:
      print(f"An error occurred: {e}")
  GPIO.cleanup()  # Clean up GPIO settings on exit

if __name__ == "__main__":
  main()