from src.gpio.gpio_controller import GPIOController
from RPi import GPIO
from src.lcd.implementations.charlcd_writer import CharLCDWriter
from src.lcd.lcd_service import LCDService
from src.reader.implementations.mfrc522_reader import MFRC522Reader
from src.reader.reader_service import ReaderService
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RED_LED_PIN = 5
GREEN_LED_PIN = 6
BUZZER_PIN = 16

class RFIDService:
    """
    RFID Service to handle RFID reading and interaction with other components.
    """
    def __init__(self):
        self.red_led = GPIOController(GPIO, RED_LED_PIN)
        self.green_led = GPIOController(GPIO, GREEN_LED_PIN)
        self.buzzer = GPIOController(GPIO, BUZZER_PIN, component_type="BUZZER")

        self.lcd_writer = CharLCDWriter(
            i2c_expander='PCF8574',
            address=0x27,
        )
        self.lcd_service = LCDService(self.lcd_writer)

        self.reader = MFRC522Reader()
        self.reader_service = ReaderService(
            reader=self.reader,
        )
        self.current_tags = set()
        self.is_reading = False
        self._start()
    
    def _start(self):
        """Start the RFID service"""
        self.red_led.turn_on()
        self.green_led.turn_off()
        self.lcd_service.write("RFID Reader started")

    def loop(self):
        """Main loop to read RFID tags and interact with components"""
        while True:
            try:
                # Turn green LED if there are tags on the reader
                if self.current_tags:
                    self.green_led.turn_on()
                    self.red_led.turn_off()
                else:
                    self.red_led.turn_on()
                    self.green_led.turn_off()
                logger.info(f"Current tags: {self.current_tags}")
                tag_id, tag_text = self.reader_service.read()
                if tag_id is not None:
                    tag_id_hashable = tuple(tag_id) if isinstance(tag_id, list) else tag_id
                    logger.info(f"Tag read: {tag_id_hashable}, Text: {tag_text}")
                    if tag_id_hashable not in self.current_tags:
                        self.current_tags.add(tag_id_hashable)
                        self.lcd_service.clear()
                        self.buzzer.turn_on()
                        sleep(0.1)  # Buzzer on for 0.1 seconds
                        self.buzzer.turn_off()
                        self.lcd_service.write("Welcome!")
                    else:
                        self.lcd_service.write(f"Goodbye {tag_text}!")
                        self.current_tags.remove(tag_id_hashable)
                else:
                    sleep(0.5)  # No tag read, wait before next attempt
            except Exception as e:
                logger.error(f"An error occurred: {e}")
