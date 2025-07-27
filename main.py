from RPi import GPIO
from src.rfid_service import RFIDService

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        rfid_service = RFIDService()
        rfid_service.loop()
    except KeyboardInterrupt:
      print("Exiting...")
    except Exception as e:
      print(f"An error occurred: {e}")
    finally:
        GPIO.cleanup()  # Clean up GPIO settings on exit
        logger.info("RFID service stopped and GPIO cleaned up.")

if __name__ == "__main__":
  main()