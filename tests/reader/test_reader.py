import pytest
from unittest import mock
from src.reader.reader_service import ReaderService

class TestReaderService:
  """
  TestReaderService is a test class for the ReaderService implementation.
  This test class verifies the behavior of the ReaderService, ensuring that:
  - Card reading functionality works correctly
  - GPIO cleanup occurs properly even when exceptions are raised
  The tests use mock objects to simulate the hardware components, allowing
  for isolated testing of the service logic.
  Attributes:
    mock_reader (MagicMock): Mock object for the RFID reader hardware
    mock_gpio (MagicMock): Mock object for the Raspberry Pi GPIO interface
    reader (ReaderService): The ReaderService instance being tested
  """
  def setup_method(self):
    self.mock_reader = mock.MagicMock()
    self.mock_gpio = mock.MagicMock()
    self.reader = ReaderService(
      reader=self.mock_reader,  # Mock the reader library
      gpio=self.mock_gpio,     # Mock the GPIO library
      is_raspberry_pi=True      # Set to True for testing
    )

  def teardown_method(self):
    pass

  def test_read_returns_id_and_text(self):
    """
    Test that the reader.read() method correctly returns both ID and text.
    This test verifies that:
    1. The read method properly unpacks the ID and text values returned by the underlying RFID reader
    2. The GPIO cleanup is called once after reading
    3. The underlying reader's read method is called once
    4. The returned ID and text match the expected values
    Returns:
      None
    """
    # Arrange
    expected_id = 12345
    expected_text = "test card"
    self.mock_reader.read.return_value = (expected_id, expected_text)
    
    # Act
    id, text = self.reader.read()

    # Assert
    self.mock_reader.read.assert_called_once()
    self.mock_gpio.cleanup.assert_called_once()
    assert id == expected_id
    assert text == expected_text

  def test_read_cleans_up_gpio_on_exception(self):
    """
    Test that GPIO resources are properly cleaned up when an exception occurs during reading.
    This test verifies that the reader calls GPIO.cleanup() even when an exception is raised
    during the reading process, ensuring that hardware resources are properly released.
    Raises:
      Exception: Deliberately raised to test exception handling
    """
    # Arrange
    self.mock_reader.read.side_effect = Exception("Test exception")
    
    with pytest.raises(Exception):
      self.reader.read()
    
    # Verify GPIO cleanup was called even with exception
    self.mock_gpio.cleanup.assert_called_once()

  def test_read_does_not_cleanup_gpio_when_not_raspberry_pi(self):
    """
    Test that GPIO cleanup is not called when is_raspberry_pi is False.
    This test ensures that the GPIO cleanup logic is only executed when
    the service is configured to run on a Raspberry Pi.
    Returns:
      None
    """
    # Arrange
    reader_service = ReaderService(
      reader=self.mock_reader,
      gpio=self.mock_gpio,
      is_raspberry_pi=False  # Set to False for this test
    )
    self.mock_reader.read.return_value = (12345, "test card")
    
    # Act
    reader_service.read()

    # Assert
    self.mock_gpio.cleanup.assert_not_called()