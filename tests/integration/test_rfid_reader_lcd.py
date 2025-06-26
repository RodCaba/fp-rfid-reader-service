import pytest
from time import sleep
from src.reader.reader_service import ReaderService
from src.lcd.lcd_service import LCDService

@pytest.mark.integration
class TestReaderLCDIntegration:
    """
    Integration tests between Reader and LCD services
    
    These tests verify that the ReaderService and LCDService work correctly
    together in various scenarios.
    """
    
    def test_successful_read_updates_lcd(self, mock_reader, mock_writer):
        """
        Test that a successful card read properly updates the LCD display
        """
        # Set up services
        reader_service = ReaderService(reader=mock_reader)
        lcd_service = LCDService(writer=mock_writer)
        
        # Simulate a read operation
        uid, text = reader_service.read()
        
        # Update LCD with the result
        if uid is not None:
            lcd_service.clear()
            lcd_service.write(f"Card: {text}")
        
        # Verify interaction
        assert mock_reader.read_called
        assert mock_reader.cleanup_called
        assert mock_writer.cleared
        assert f"Card: {mock_reader.text}" in mock_writer.written_text
