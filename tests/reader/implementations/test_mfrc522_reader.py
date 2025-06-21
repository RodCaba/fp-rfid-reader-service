import pytest
from unittest.mock import MagicMock, patch
from src.reader.implementations.mfrc522_reader import MFRC522Reader

@pytest.fixture
def mock_mfrc522():
  with patch('src.reader.implementations.mfrc522_reader.MFRC522') as mock_class:
    mock_instance = MagicMock()
    mock_class.return_value = mock_instance
    yield mock_instance

@pytest.fixture
def reader(mock_mfrc522):
  return MFRC522Reader()

class TestMFRC522Reader:
  """
  Test suite for the MFRC522Reader class.
  This class tests the functionality of the MFRC522Reader which interacts with the MFRC522 RFID reader module.
  Tests:
    - Initialization of the MFRC522Reader object
    - Successful tag reading operation
    - Error handling when no tag is detected
    - Error handling when anti-collision procedure fails
    - Proper cleanup of GPIO resources
  Fixtures:
    - mock_mfrc522: Mocks the MFRC522 module
    - reader: Provides a configured MFRC522Reader instance for testing
  """
  
  def test_init(self, mock_mfrc522):
    """
    Tests the initialization of the MFRC522Reader.
    This test verifies that the MFRC522Reader is correctly instantiated with a mocked MFRC522 object.
    """
    reader = MFRC522Reader()
    assert reader.reader == mock_mfrc522
    
  def test_read_success(self, reader, mock_mfrc522):
    """
    Tests the successful reading of an RFID tag using the MFRC522 reader.
    This test mocks the MFRC522 hardware interface to simulate a successful card read operation.
    """
    # Set up mock return values
    mock_mfrc522.MI_OK = 0
    mock_mfrc522.PICC_REQIDL = 1
    mock_mfrc522.MFRC522_Request.return_value = (0, "some_tag_type")
    mock_mfrc522.MFRC522_Anticoll.return_value = (0, [1, 2, 3, 4, 5])
    
    # Call the method
    uid, text = reader.read()
    
    # Assertions
    assert uid == [1, 2, 3, 4, 5]
    assert text == "Sample Text"
    mock_mfrc522.MFRC522_Request.assert_called_once_with(mock_mfrc522.PICC_REQIDL)
    mock_mfrc522.MFRC522_Anticoll.assert_called_once()
    
  def test_read_no_tag_detected(self, reader, mock_mfrc522):
    """
    Test behavior when no tag is detected during a read operation.
    This test verifies that when the MFRC522 reader doesn't detect a tag
    (indicated by MFRC522_Request returning a status code that's not MI_OK),
    the read() method raises an exception with the message "No tag detected".
    The test also confirms that:
    1. MFRC522_Request is called exactly once
    2. MFRC522_Anticoll is never called since tag detection fails earlier
    """
    # Set up mock return values for no tag detection
    mock_mfrc522.MI_OK = 0
    mock_mfrc522.PICC_REQIDL = 1
    mock_mfrc522.MFRC522_Request.return_value = (1, None)  # Not MI_OK
    
    # Call the method and check for exception
    with pytest.raises(Exception) as exc_info:
      reader.read()
    
    assert str(exc_info.value) == "No tag detected"
    mock_mfrc522.MFRC522_Request.assert_called_once()
    mock_mfrc522.MFRC522_Anticoll.assert_not_called()
    
  def test_read_anticoll_failed(self, reader, mock_mfrc522):
    """Test that the MFRC522 reader raises an exception when tag anticollision fails.
    This test verifies that when the anticollision phase of the RFID reading process
    fails (returns a status code other than MI_OK), the reader properly raises 
    an exception with the message "Failed to read UID from tag".
    The test mocks:
    - A successful tag detection (Request returns MI_OK)
    - A failed anticollision procedure (Anticoll returns non-MI_OK)
    It also verifies that both the Request and Anticoll methods are called exactly once.
    """
    # Set up mock return values for anticoll failure
    mock_mfrc522.MI_OK = 0
    mock_mfrc522.PICC_REQIDL = 1
    mock_mfrc522.MFRC522_Request.return_value = (0, "some_tag_type")
    mock_mfrc522.MFRC522_Anticoll.return_value = (1, None)  # Not MI_OK
    
    # Call the method and check for exception
    with pytest.raises(Exception) as exc_info:
      reader.read()
    
    assert str(exc_info.value) == "Failed to read UID from tag"
    mock_mfrc522.MFRC522_Request.assert_called_once()
    mock_mfrc522.MFRC522_Anticoll.assert_called_once()