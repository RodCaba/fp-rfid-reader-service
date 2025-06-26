import sys
import pytest
from unittest.mock import MagicMock

# Create mocks for hardware-dependent modules
mock_GPIO = MagicMock()
mock_spidev = MagicMock()
mock_mfrc522 = MagicMock()
mock_smbus2 = MagicMock()
mock_rplcd = MagicMock()

# Add mocks to sys.modules before any tests run
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = mock_GPIO
sys.modules['spidev'] = mock_spidev
sys.modules['mfrc522'] = mock_mfrc522
sys.modules['smbus2'] = mock_smbus2
sys.modules['rplcd'] = mock_rplcd

@pytest.fixture
def gpio():
    """Provide access to the mocked GPIO module."""
    return mock_GPIO

@pytest.fixture
def spidev():
    """Provide access to the mocked SPI module."""
    return mock_spidev

@pytest.fixture
def mfrc522():
    """Provide access to the mocked MFRC522 module."""
    return mock_mfrc522

@pytest.fixture
def smbus2():
    """Provide access to the mocked SMBus2 module."""
    return mock_smbus2

@pytest.fixture
def rplcd():
    """Provide access to the mocked RPLCD module."""
    return mock_rplcd

# INTEGRATION TEST FIXTURES

@pytest.fixture
def mock_reader():
    """Mock RFID reader that returns predictable data"""
    from src.reader.base import Reader
    
    class MockReader(Reader):
        def __init__(self, uid=None, text=None):
            self.uid = uid or [1, 2, 3, 4, 5]
            self.text = text or "Test Card"
            self.read_called = False
            self.cleanup_called = False
            
        def read(self):
            self.read_called = True
            return self.uid, self.text
            
        def cleanup(self):
            self.cleanup_called = True
    
    return MockReader()

@pytest.fixture
def mock_writer():
    """Mock LCD writer for testing"""
    from src.lcd.base import Writer
    
    class MockWriter(Writer):
        def __init__(self):
            super().__init__()
            self.written_text = []
            self.cleared = False
            
        def write(self, text):
            self.written_text.append(text)
            
        def clear(self):
            self.cleared = True
            self.written_text = []
    
    return MockWriter()

@pytest.fixture
def gpio_controller():
    """Fixture for a GPIO controller using the mocked GPIO"""
    from src.gpio.gpio_controller import GPIOController
    return lambda pin, component_type="LED": GPIOController(gpio=mock_GPIO, pin=pin, component_type=component_type)