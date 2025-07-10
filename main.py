from src.reader.reader_service import ReaderService
from src.reader.implementations.mfrc522_reader import MFRC522Reader

from src.lcd.lcd_service import LCDService
from src.lcd.implementations.charlcd_writer import CharLCDWriter

from src.gpio.gpio_controller import GPIOController
from src.audio_client import AudioServiceClient
from RPi import GPIO
from time import sleep
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

  # Initialize audio service client (uses AUDIO_SERVICE_URL env var)
  audio_client = AudioServiceClient()
  
  # Wait for audio service to be available
  lcd_service.write("Waiting for audio...")
  if not audio_client.wait_for_service():
    lcd_service.write("Audio service unavailable")
    logger.error("Audio service is not available")
  else:
    lcd_service.write("Audio service ready")
    sleep(2)
    lcd_service.clear()

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
        sleep(0.1)  # Buzzer on for 0.1 seconds
        buzzer.turn_off()
        if not IS_READING:
          lcd_service.write("Welcome!")
          IS_READING = True
          red_led.turn_off()
          green_led.turn_on()

          while IS_READING:
            # Trigger audio recording and prediction via gRPC
            lcd_service.write("Processing audio...")
            logger.info("Triggering audio recording and prediction via gRPC")
            
            try:
              result = audio_client.start_audio_processing(duration=5)
              if result and result.get('success'):
                predicted_class = result.get('predicted_class', 'Unknown')
                confidence = result.get('confidence', 0)
                
                # Display prediction on LCD
                lcd_service.clear()
                lcd_service.write(f"Audio: {predicted_class}")
                sleep(2)
                lcd_service.write(f"Confidence: {confidence:.2f}")
                
                logger.info(f"Audio prediction: {predicted_class} (confidence: {confidence:.2f})")
              else:
                lcd_service.write("Audio processing failed")
                error_msg = result.get('error_message', 'Unknown error') if result else 'No response'
                logger.error(f"Audio processing failed: {error_msg}")

              try:
                id, text = reader_service.read()
                if id is not None:
                  lcd_service.write("Goodbye!")
                  IS_READING = False
                  red_led.turn_on()
                  green_led.turn_off()
                  sleep(2)
                  lcd_service.clear()
              except Exception as e:
                lcd_service.write("Error reading tag")
                logger.error(f"Error reading tag: {e}")
            except Exception as e:
              lcd_service.write("Audio error")
              logger.error(f"Audio processing error: {e}")
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
  
  # Close audio client connection
  try:
    audio_client.close()
  except:
    pass

if __name__ == "__main__":
  main()