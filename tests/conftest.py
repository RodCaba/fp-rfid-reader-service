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
