from unittest.mock import Mock, patch
from src.lcd.lcd_service import LCDService
from src.lcd.base import Writer

class TestLCDService:
  """
  TestLCDService class for testing the LCD service functionality.
  This test class verifies the functionality of the LCDService class by mocking
  the Writer component and validating:
  - Proper initialization of the service
  - Writing text to the LCD display works correctly 
  - Error handling when writing fails
  """
  def setup_method(self):
    self.mock_writer = Mock(spec=Writer)
    self.lcd_service = LCDService(self.mock_writer)

  def test_init(self):
    """
    Test that the LCDService is initialized with the correct writer.
    """
    assert self.lcd_service.writer == self.mock_writer

  def test_write_calls_writer_write(self):
    """
    Test that the write method calls the writer's write method with the correct text.
    """
    test_text = "Hello, LCD!"
    self.lcd_service.write(test_text)
    self.mock_writer.write.assert_called_once_with(test_text)

  def test_write_handles_exception(self):
    """
    Test that the write method handles exceptions raised by the writer's write method.
    """
    test_text = "Error test"
    self.mock_writer.write.side_effect = Exception("Test exception")
    
    with patch("builtins.print") as mock_print:
      self.lcd_service.write(test_text)
      mock_print.assert_called_with("Error writing to LCD: Test exception")