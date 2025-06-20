from src.reader.reader_service import ReaderService
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def main():
  while True:
    try:
      run_reader_service()
    except KeyboardInterrupt:
      print("Exiting...")
      break
    except Exception as e:
      print(f"An error occurred: {e}")

def run_reader_service():
  reader = SimpleMFRC522()
  gpio = GPIO
  reader_service = ReaderService(
    reader=reader,
    gpio=gpio,
    is_raspberry_pi=True  # Set to True for Raspberry Pi
  )
  reader_service.read()

if __name__ == "__main__":
  main()