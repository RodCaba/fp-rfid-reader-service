import pytest
from unittest import mock
from src.reader.reader_service import ReaderService
from src.reader.base import Reader

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
    reader (ReaderService): The ReaderService instance being tested
  """
  def setup_method(self):
    # Use unittest.mock to create a mock reader
    self.mock_reader = mock.MagicMock(spec=Reader)
    
    # Configure the mock's default return value for read()
    self.mock_reader.read.return_value = (12345, "test card")
    
    self.reader = ReaderService(
      reader=self.mock_reader,
      is_raspberry_pi=True      # Set to True for testing
    )

  def teardown_method(self):
    pass

  def test_read_returns_id_and_text(self):
    """
    Test that the reader.read() method correctly returns both ID and text.
    """
    # Act
    id, text = self.reader.read()

    # Assert
    self.mock_reader.read.assert_called_once()
    self.mock_reader.cleanup.assert_called_once()
    assert id == 12345
    assert text == "test card"

  def test_read_cleans_up_gpio_on_exception(self):
    """
    Test that GPIO resources are properly cleaned up when an exception occurs during reading.
    """
    # Arrange - reconfigure the mock to raise an exception
    self.mock_reader.read.side_effect = Exception("Test exception")
    
    with pytest.raises(Exception):
      self.reader.read()
    
    # Verify cleanup was called even with exception
    self.mock_reader.cleanup.assert_called_once()