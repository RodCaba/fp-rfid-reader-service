import grpc
import time
import uuid
import logging
from typing import Dict, Optional

from src.grpc_generated import audio_service_pb2
from src.grpc_generated import audio_service_pb2_grpc


class AudioClient:
    """gRPC client for Audio Processing Service"""
    
    def __init__(self, server_address: str = "audio-service:50051", timeout: int = 30):
        self.server_address = server_address
        self.timeout = timeout
        self.channel = None
        self.stub = None
        self.logger = logging.getLogger(__name__)
        
        self._connect()
    
    def _connect(self):
        """Establish connection to audio service"""
        try:
            self.channel = grpc.insecure_channel(self.server_address)
            self.stub = audio_service_pb2_grpc.AudioServiceStub(self.channel)
            self.logger.info(f"Connected to audio service at {self.server_address}")
        except Exception as e:
            self.logger.error(f"Failed to connect to audio service: {e}")
            raise
    
    def health_check(self) -> bool:
        """Check if the audio service is healthy"""
        try:
            request = audio_service_pb2.HealthCheckRequest()
            response = self.stub.HealthCheck(request, timeout=5)
            return response.status == "SERVING"
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    def wait_for_service(self, max_retries: int = 10, retry_delay: int = 2) -> bool:
        """Wait for the audio service to become available"""
        for attempt in range(max_retries):
            if self.health_check():
                self.logger.info("Audio service is ready")
                return True
            
            self.logger.info(f"Waiting for audio service... (attempt {attempt + 1}/{max_retries})")
            time.sleep(retry_delay)
        
        self.logger.error("Audio service did not become available")
        return False
    
    def start_audio_processing(self, duration: int = 5, session_id: Optional[str] = None) -> Optional[Dict]:
        """
        Start audio recording and processing
        
        Args:
            duration: Recording duration in seconds
            session_id: Optional session ID (will generate if not provided)
            
        Returns:
            Dict with processing results or None if failed
        """
        try:
            if session_id is None:
                session_id = str(uuid.uuid4())
            
            request = audio_service_pb2.AudioRequest(
                session_id=session_id,
                recording_duration=duration,
                output_format="wav"
            )
            
            response = self.stub.StartAudioProcessing(request, timeout=self.timeout)
            
            if response.success:
                # Convert protobuf response to dict
                top_predictions = []
                for pred in response.top_predictions:
                    top_predictions.append({
                        'class_name': pred.class_name,
                        'probability': pred.probability
                    })
                
                return {
                    'session_id': response.session_id,
                    'success': True,
                    'predicted_class': response.predicted_class,
                    'confidence': response.confidence,
                    'top_predictions': top_predictions
                }
            else:
                self.logger.error(f"Audio processing failed: {response.error_message}")
                return {
                    'session_id': response.session_id,
                    'success': False,
                    'error_message': response.error_message
                }
                
        except Exception as e:
            self.logger.error(f"Failed to start audio processing: {e}")
            return None
    
    def get_processing_status(self, session_id: str) -> Optional[Dict]:
        """
        Get the status of audio processing
        
        Args:
            session_id: Session ID to check
            
        Returns:
            Dict with status information or None if failed
        """
        try:
            request = audio_service_pb2.StatusRequest(session_id=session_id)
            response = self.stub.GetProcessingStatus(request, timeout=5)
            
            return {
                'session_id': response.session_id,
                'status': response.status,
                'current_operation': response.current_operation
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get processing status: {e}")
            return None
    
    def close(self):
        """Close the gRPC channel"""
        if self.channel:
            self.channel.close()
            self.logger.info("Audio service connection closed")
