from src.reader.reader_service import ReaderService
from src.reader.implementations.mfrc522_reader import MFRC522Reader

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
  reader = MFRC522Reader()
  reader_service = ReaderService(
    reader=reader,
    is_raspberry_pi=True  # Set to True for Raspberry Pi
  )
  reader_service.read()

if __name__ == "__main__":
  main()