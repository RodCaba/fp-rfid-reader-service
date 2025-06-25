# RFID Service

A Python service for interfacing with RFID readers on Raspberry Pi devices.

## Overview

This service provides a simple interface for reading RFID tags using the MFRC522 RFID reader module connected to a Raspberry Pi. The service handles proper GPIO resource management to ensure clean operation even when exceptions occur.

## Requirements

- Python 3.10+
- Raspberry Pi with GPIO pins
- MFRC522 RFID reader module
- SPI interface enabled on Raspberry Pi
- I2C character LCD display

## Dependencies

```
spidev==3.7
mfrc522==0.0.7
RPLCD==1.3.1
pytest==8.4.1
pytest-mock==3.14.1
```

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd rfid-service
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Connect the MFRC522 RFID reader to your Raspberry Pi according to the following pin mapping:
   - SDA -> Pin 24
   - SCK -> Pin 23
   - MOSI -> Pin 19
   - MISO -> Pin 21
   - GND -> Pin 6
   - RST -> Pin 22
   - 3.3V -> Pin 1

4. Connect the I2C LCD display:
   - SDA -> Pin 3 (GPIO 2)
   - SCL -> Pin 5 (GPIO 3)
   - VCC -> 5V
   - GND -> GND

## Usage

### Basic Usage

Run the main script to read an RFID tag:

```
python main.py
```

### Advanced Usage

The service is structured using abstractions and dependency injection, which makes it easy to extend with new reader types or LCD displays.

Example custom implementation:

```python
from src.reader.base import Reader
from src.reader.reader_service import ReaderService

# Create a custom reader implementation
class MyCustomReader(Reader):
    def read(self):
        # Custom implementation
        return 12345, "My custom tag"
        
    def cleanup(self):
        # Custom cleanup
        pass

# Use it with the reader service
reader = MyCustomReader()
reader_service = ReaderService(reader=reader)
id, text = reader_service.read()
```

## Testing

Tests are written using pytest. The testing architecture uses mocks to simulate hardware dependencies, allowing tests to run on non-Raspberry Pi environments.

### Running Tests

```
pytest
```

Or to run specific tests:

```
pytest tests/reader/test_reader_service.py
```

### Continuous Integration

This project includes GitHub Actions workflows that automatically run tests on every push to master or pull request:

```yaml
name: Run Python Tests
on:
  push:
    branches: [ master, main ]
  pull_request:
    branches: [ master, main ]
```

### Writing Tests

To write tests for hardware-dependent components, utilize the mock objects provided by the conftest.py fixtures:

```python
def test_reader_function(mock_mfrc522):
    # Configure the mock
    mock_mfrc522.read.return_value = (12345, "test")
    
    # Test your code
    reader = YourReader()
    result = reader.read()
    
    # Assert expected behavior
    assert result == (12345, "test")
```

## Project Structure

- `src/` - Source code
  - `reader/` - RFID reader abstraction and implementations
  - `lcd/` - LCD display abstraction and implementations
  - `gpio/` - GPIO control utilities
- `tests/` - Test suites
  - `conftest.py` - Global test configuration and mocks
  - `reader/` - Reader tests
  - `lcd/` - LCD tests
  - `gpio/` - GPIO controller tests
- `main.py` - Simple demonstration script
- `.github/workflows/` - CI/CD configuration

## Features

- Clean GPIO resource management
- Exception handling
- Configurable for non-Raspberry Pi environments (for testing)
- Comprehensive test suite
- Dependency injection for easy component swapping
- Abstract interfaces for readers and displays