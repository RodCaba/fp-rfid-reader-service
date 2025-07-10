"""
RFID Service Simulator - For testing without hardware
Simulates RFID card detection and communicates with audio service via gRPC
"""

import time
import logging
import uuid
import threading
from src.audio_client import AudioServiceClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RFIDSimulator:
    """Simulate RFID reader behavior for testing"""
    
    def __init__(self):
        self.is_reading = False
        self.simulation_interval = 10  # seconds between simulated card detections
        
        # Initialize audio service client (uses AUDIO_SERVICE_URL env var)
        self.audio_client = AudioServiceClient()
    
    def simulate_lcd_write(self, message):
        """Simulate LCD display"""
        print(f"[LCD] {message}")
    
    def simulate_led_control(self, led_color, state):
        """Simulate LED control"""
        print(f"[LED] {led_color} LED: {'ON' if state else 'OFF'}")
    
    def simulate_buzzer(self, duration=0.1):
        """Simulate buzzer sound"""
        print(f"[BUZZER] BEEP for {duration}s")
        time.sleep(duration)
    
    def audio_processing_loop(self):
        """Continuously process audio in background while is_reading is True"""
        while self.is_reading:
            try:
                # Trigger audio recording and prediction via gRPC
                self.simulate_lcd_write("Processing audio...")
                logger.info("Triggering audio recording and prediction via gRPC")
                
                result = self.audio_client.start_audio_processing(duration=5)
                if result and result.get('success'):
                    predicted_class = result.get('predicted_class', 'Unknown')
                    confidence = result.get('confidence', 0)
                    top_predictions = result.get('top_predictions', [])
                    
                    # Display prediction results
                    self.simulate_lcd_write(f"Audio: {predicted_class}")
                    time.sleep(2)
                    self.simulate_lcd_write(f"Confidence: {confidence:.2f}")
                    
                    logger.info(f"Audio prediction: {predicted_class} (confidence: {confidence:.2f})")
                    logger.info(f"Top predictions: {top_predictions}")
                else:
                    self.simulate_lcd_write("Audio processing failed")
                    error_msg = result.get('error_message', 'Unknown error') if result else 'No response'
                    logger.error(f"Audio processing failed: {error_msg}")
                
                # Small delay before next iteration (only if still reading)
                if self.is_reading:
                    time.sleep(1)
                    
            except Exception as e:
                self.simulate_lcd_write("Audio error")
                logger.error(f"Audio processing error: {e}")
                if self.is_reading:
                    time.sleep(1)
        
        # When exiting the loop, clear the display
        self.simulate_lcd_write("")  # Clear display
        logger.info("Audio processing loop ended")
    
    def wait_for_audio_service(self):
        """Wait for audio service to be available"""
        self.simulate_lcd_write("Waiting for audio...")
        if not self.audio_client.wait_for_service():
            self.simulate_lcd_write("Audio service unavailable")
            logger.error("Audio service is not available")
            return False
        else:
            self.simulate_lcd_write("Audio service ready")
            time.sleep(2)
            self.simulate_lcd_write("")  # Clear display
            return True
    
    def simulate_rfid_detection(self):
        """Simulate RFID card detection"""
        card_id = f"CARD_{uuid.uuid4().hex[:8].upper()}"
        logger.info(f"Simulating RFID card detection: {card_id}")
        
        # Simulate buzzer
        self.simulate_buzzer()
        
        if not self.is_reading:
            self.simulate_lcd_write("Welcome!")
            self.is_reading = True
            self.simulate_led_control("RED", False)
            self.simulate_led_control("GREEN", True)
            
            # Start audio processing in background thread
            audio_thread = threading.Thread(target=self.audio_processing_loop)
            audio_thread.daemon = True  # Thread will exit when main program exits
            audio_thread.start()
            
        else:
            # Second RFID swipe - stop the audio processing
            self.simulate_lcd_write("Goodbye!")
            self.is_reading = False  # This will cause the background loop to exit
            self.simulate_led_control("RED", True)
            self.simulate_led_control("GREEN", False)
        
        time.sleep(3)
        self.simulate_lcd_write("")  # Clear display
    
    def run_simulation(self):
        """Run the RFID simulation"""
        print("=== RFID Service Simulator Started ===")
        self.simulate_lcd_write("RFID Reader started")
        
        # Initialize LED states
        self.simulate_led_control("RED", True)
        self.simulate_led_control("GREEN", False)
        
        # Wait for audio service
        if not self.wait_for_audio_service():
            logger.error("Cannot continue without audio service")
            return
        
        try:
            iteration = 1
            while True:
                print(f"\n--- Simulation Iteration {iteration} ---")
                print(f"Simulating RFID card detection in 3 seconds...")
                time.sleep(3)
                
                self.simulate_rfid_detection()
                
                print(f"Waiting {self.simulation_interval} seconds before next simulation...")
                time.sleep(self.simulation_interval)
                iteration += 1
                
        except KeyboardInterrupt:
            print("\n=== Simulation stopped by user ===")
        finally:
            # Cleanup
            try:
                self.audio_client.close()
            except:
                pass
            print("Simulation cleanup completed")


def main():
    """Main entry point for simulator"""
    simulator = RFIDSimulator()
    simulator.run_simulation()


if __name__ == "__main__":
    main()
