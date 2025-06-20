# RFID Service

A Python service for interfacing with RFID readers on Raspberry Pi devices.

## Overview

This service provides a simple interface for reading RFID tags using the MFRC522 RFID reader module connected to a Raspberry Pi. The service handles proper GPIO resource management to ensure clean operation even when exceptions occur.

## Requirements

- Python 3.10+
- Raspberry Pi with GPIO pins
- MFRC522 RFID reader module
- SPI interface enabled on Raspberry Pi

## Dependencies

```
spidev==3.7
mfrc522==0.0.7
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

## Usage

### Basic Usage

Run the main script to read an RFID tag:

```
python main.py
```

## Testing

Tests are written using pytest. To run the tests:

```
pytest
```

Or to run specific tests:

```
pytest tests/reader/test_reader.py
```

## Project Structure

- `src/reader/` - Contains the core reader service implementation
- `tests/` - Contains unit tests
- `main.py` - Simple demonstration script

## Features

- Clean GPIO resource management
- Exception handling
- Configurable for non-Raspberry Pi environments (for testing)
- Comprehensive test suite
