import pytest
from unittest.mock import MagicMock, patch
from src.lcd.implementations.charlcd_writer import CharLCDWriter

@pytest.fixture
def mock_charlcd():
  with patch('src.lcd.implementations.charlcd_writer.CharLCD') as mock_class:
    mock_instance = MagicMock()
    mock_class.return_value = mock_instance
    yield mock_instance

@pytest.fixture
def writer(mock_charlcd):
  return CharLCDWriter(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=16,
    rows=2,
    dotsize=8
  )

class TestCharLCDWriter:
  def test_init(self, mock_charlcd):
    # Test the initialization of CharLCDWriter
    writer = CharLCDWriter(
      i2c_expander='PCF8574',
      address=0x27,
      port=1,
      cols=16,
      rows=2,
      dotsize=8
    )
    
    assert writer.lcd == mock_charlcd

  def test_release(self, writer, mock_charlcd):
    # Test the cleanup of CharLCDWriter
    writer.__del__()
    
    mock_charlcd.clear.assert_called_once()
    
  def test_write_success(self, writer, mock_charlcd):
    # Test successful write operation
    writer.write("Hello, World!")
    
    mock_charlcd.write_string.assert_called_once_with("Hello, World!")
    
  def test_write_exception(self, writer, mock_charlcd):
    # Test exception handling in write method
    mock_charlcd.write_string.side_effect = Exception("Test error")
    
    with pytest.raises(Exception) as excinfo:
      writer.write("Hello, World!")
    
    assert "Error writing to LCD: Test error" in str(excinfo.value)
    
  def test_clear_success(self, writer, mock_charlcd):
    # Test successful clear operation
    writer.clear()
    
    mock_charlcd.clear.assert_called_once()
    
  def test_clear_exception(self, writer, mock_charlcd):
    mock_charlcd.clear.side_effect = Exception("Test error")
    
    with pytest.raises(Exception) as excinfo:
      writer.clear()
    
    assert "Error clearing LCD: Test error" in str(excinfo.value)