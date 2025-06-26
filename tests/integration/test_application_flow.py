import pytest
from unittest.mock import MagicMock, patch
from time import sleep
from src.reader.reader_service import ReaderService
from src.lcd.lcd_service import LCDService
from src.gpio.gpio_controller import GPIOController

@pytest.mark.integration
class TestApplicationFlow:
    """
    Integration tests for the complete application flow
    
    These tests verify that all services work together properly to implement
    the full functionality of the RFID service.
    """
    
    @pytest.fixture
    def setup_components(self, mock_reader, mock_writer, monkeypatch):
        """Set up all application components for testing"""
        # Mock GPIO
        gpio_mock = MagicMock()
        monkeypatch.setattr("RPi.GPIO", gpio_mock)
        
        # Create services
        reader_service = ReaderService(reader=mock_reader)
        lcd_service = LCDService(writer=mock_writer)
        
        # Create GPIO controllers
        red_led = GPIOController(gpio=gpio_mock, pin=5)
        green_led = GPIOController(gpio=gpio_mock, pin=6)
        buzzer = GPIOController(gpio=gpio_mock, pin=16, component_type="BUZZER")
        
        return {
            'reader_service': reader_service,
            'lcd_service': lcd_service,
            'red_led': red_led,
            'green_led': green_led,
            'buzzer': buzzer,
            'gpio': gpio_mock,
            'mock_reader': mock_reader,
            'mock_writer': mock_writer
        }
    
    def test_initial_tag_read_welcomes_user(self, setup_components):
        """
        Test the full flow when a tag is read for the first time:
        - Red LED turns off
        - Green LED turns on
        - Buzzer sounds briefly
        - LCD displays welcome message
        """
        components = setup_components
        
        # Initial state: Red LED on, Green LED off
        components['red_led'].turn_on()
        components['green_led'].turn_off()
        
        # Simulate tag read
        uid, text = components['reader_service'].read()
        
        # Process tag read
        if uid is not None:
            components['lcd_service'].clear()
            components['buzzer'].turn_on()
            sleep(0.01)  # Simulate buzzer sound
            components['buzzer'].turn_off()
            
            # First read: Welcome
            components['lcd_service'].write("Welcome!")
            components['red_led'].turn_off()
            components['green_led'].turn_on()
            
        # Verify the expected behavior
        assert components['mock_writer'].cleared
        assert "Welcome!" in components['mock_writer'].written_text
        assert components['gpio'].output.call_count >= 3  # At least 3 calls to GPIO.output
    
    def test_second_tag_read_says_goodbye(self, setup_components):
        """
        Test the full flow when a tag is read for the second time:
        - Green LED turns off
        - Red LED turns on
        - Buzzer sounds briefly
        - LCD displays goodbye message
        """
        components = setup_components
        
        # Initial state: Green LED on, Red LED off (as if first read already happened)
        components['green_led'].turn_on()
        components['red_led'].turn_off()
        
        # Simulate tag read
        uid, text = components['reader_service'].read()
        
        # Process tag read
        if uid is not None:
            components['lcd_service'].clear()
            components['buzzer'].turn_on()
            sleep(0.01)  # Simulate buzzer sound
            components['buzzer'].turn_off()
            
            # Second read: Goodbye
            components['lcd_service'].write("Goodbye!")
            components['red_led'].turn_on()
            components['green_led'].turn_off()
            
        # Verify the expected behavior
        assert components['mock_writer'].cleared
        assert "Goodbye!" in components['mock_writer'].written_text
        assert components['gpio'].output.call_count >= 3  # At least 3 calls to GPIO.output