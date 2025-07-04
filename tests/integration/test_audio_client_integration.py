import pytest
import grpc
import threading
import time
import uuid
from concurrent import futures
from unittest.mock import Mock

from src.grpc_generated import audio_service_pb2
from src.grpc_generated import audio_service_pb2_grpc
from src.audio_client import AudioServiceClient


class MockAudioServiceServer(audio_service_pb2_grpc.AudioServiceServicer):
    """Mock implementation of AudioService for testing"""
    
    def __init__(self):
        self.sessions = {}  # Store session data
        self.health_status = "SERVING"
        self.should_fail_health_check = False
        self.should_fail_processing = False
        self.processing_delay = 0
    
    def HealthCheck(self, request, context):
        """Mock health check implementation"""
        if self.should_fail_health_check:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details("Service unavailable")
            raise grpc.RpcError()
        
        return audio_service_pb2.HealthCheckResponse(
            status=self.health_status,
            message="Service is healthy"
        )
    
    def StartAudioProcessing(self, request, context):
        """Mock audio processing implementation"""
        if self.processing_delay > 0:
            time.sleep(self.processing_delay)
        
        if self.should_fail_processing:
            return audio_service_pb2.AudioResponse(
                session_id=request.session_id,
                success=False,
                error_message="Processing failed due to mock configuration"
            )
        
        # Store session data
        self.sessions[request.session_id] = {
            'status': 'completed',
            'current_operation': 'analysis_complete'
        }
        
        # Create mock predictions
        predictions = [
            audio_service_pb2.ClassProbability(class_name="bird", probability=0.85),
            audio_service_pb2.ClassProbability(class_name="car", probability=0.10),
            audio_service_pb2.ClassProbability(class_name="silence", probability=0.05)
        ]
        
        return audio_service_pb2.AudioResponse(
            session_id=request.session_id,
            success=True,
            predicted_class="bird",
            confidence=0.85,
            top_predictions=predictions
        )
    
    def GetProcessingStatus(self, request, context):
        """Mock status retrieval implementation"""
        session_data = self.sessions.get(request.session_id, {
            'status': 'not_found',
            'current_operation': 'none'
        })
        
        return audio_service_pb2.StatusResponse(
            session_id=request.session_id,
            status=session_data['status'],
            current_operation=session_data['current_operation']
        )
    
    def set_health_status(self, status: str, should_fail: bool = False):
        """Helper method to control health check behavior"""
        self.health_status = status
        self.should_fail_health_check = should_fail
    
    def set_processing_behavior(self, should_fail: bool = False, delay: float = 0):
        """Helper method to control processing behavior"""
        self.should_fail_processing = should_fail
        self.processing_delay = delay


class TestAudioClientIntegration:
    """Integration tests for AudioServiceClient using a mock gRPC server"""
    
    @pytest.fixture(autouse=True)
    def setup_mock_server(self):
        """Set up a mock gRPC server for testing"""
        # Create mock service
        self.mock_service = MockAudioServiceServer()
        
        # Create gRPC server
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        audio_service_pb2_grpc.add_AudioServiceServicer_to_server(
            self.mock_service, self.server
        )
        
        # Find an available port
        port = self.server.add_insecure_port('[::]:0')
        self.server_address = f'localhost:{port}'
        
        # Start server
        self.server.start()
        
        # Wait a bit for server to start
        time.sleep(0.1)
        
        yield
        
        # Cleanup
        self.server.stop(0)
    
    def test_client_connects_to_server(self):
        """Test that client can successfully connect to the mock server"""
        client = AudioServiceClient(server_address=self.server_address)
        
        assert client.server_address == self.server_address
        assert client.channel is not None
        assert client.stub is not None
        
        client.close()
    
    def test_health_check_integration(self):
        """Test health check with actual gRPC communication"""
        client = AudioServiceClient(server_address=self.server_address)
        
        # Test successful health check
        self.mock_service.set_health_status("SERVING")
        result = client.health_check()
        assert result is True
        
        # Test health check with non-serving status
        self.mock_service.set_health_status("NOT_SERVING")
        result = client.health_check()
        assert result is False
        
        # Test health check failure
        self.mock_service.set_health_status("SERVING", should_fail=True)
        result = client.health_check()
        assert result is False
        
        client.close()
    
    def test_wait_for_service_integration(self):
        """Test waiting for service with actual gRPC communication"""
        # Start with failing health checks
        self.mock_service.set_health_status("SERVING", should_fail=True)
        
        client = AudioServiceClient(server_address=self.server_address)
        
        # Test timeout scenario
        result = client.wait_for_service(max_retries=2, retry_delay=0.1)
        assert result is False
        
        # Test successful scenario
        self.mock_service.set_health_status("SERVING", should_fail=False)
        result = client.wait_for_service(max_retries=2, retry_delay=0.1)
        assert result is True
        
        client.close()
    
    def test_start_audio_processing_success_integration(self):
        """Test successful audio processing with actual gRPC communication"""
        client = AudioServiceClient(server_address=self.server_address)
        
        self.mock_service.set_processing_behavior(should_fail=False)
        
        result = client.start_audio_processing(duration=5)
        
        assert result is not None
        assert result['success'] is True
        assert result['predicted_class'] == "bird"
        assert abs(result['confidence'] - 0.85) < 0.001  # Account for floating point precision
        assert len(result['top_predictions']) == 3
        assert result['top_predictions'][0]['class_name'] == "bird"
        assert abs(result['top_predictions'][0]['probability'] - 0.85) < 0.001
        
        client.close()
    
    def test_start_audio_processing_failure_integration(self):
        """Test audio processing failure with actual gRPC communication"""
        client = AudioServiceClient(server_address=self.server_address)
        
        self.mock_service.set_processing_behavior(should_fail=True)
        
        result = client.start_audio_processing(duration=5)
        
        assert result is not None
        assert result['success'] is False
        assert 'error_message' in result
        assert result['error_message'] == "Processing failed due to mock configuration"
        
        client.close()
    
    def test_start_audio_processing_with_custom_session_id_integration(self):
        """Test audio processing with custom session ID"""
        client = AudioServiceClient(server_address=self.server_address)
        
        custom_session_id = "test-session-123"
        result = client.start_audio_processing(duration=3, session_id=custom_session_id)
        
        assert result is not None
        assert result['session_id'] == custom_session_id
        assert result['success'] is True
        
        client.close()
    
    def test_get_processing_status_integration(self):
        """Test getting processing status with actual gRPC communication"""
        client = AudioServiceClient(server_address=self.server_address)
        
        # First start a processing session
        result = client.start_audio_processing(duration=3)
        session_id = result['session_id']
        
        # Then get its status
        status_result = client.get_processing_status(session_id)
        
        assert status_result is not None
        assert status_result['session_id'] == session_id
        assert status_result['status'] == 'completed'
        assert status_result['current_operation'] == 'analysis_complete'
        
        client.close()
    
    def test_get_processing_status_unknown_session_integration(self):
        """Test getting status for unknown session"""
        client = AudioServiceClient(server_address=self.server_address)
        
        unknown_session_id = "unknown-session-id"
        status_result = client.get_processing_status(unknown_session_id)
        
        assert status_result is not None
        assert status_result['session_id'] == unknown_session_id
        assert status_result['status'] == 'not_found'
        assert status_result['current_operation'] == 'none'
        
        client.close()
    
    def test_processing_with_timeout_integration(self):
        """Test processing with timeout scenarios"""
        # Use a short timeout for this test
        client = AudioServiceClient(server_address=self.server_address, timeout=1)
        
        # Configure mock to take longer than timeout
        self.mock_service.set_processing_behavior(should_fail=False, delay=2)
        
        result = client.start_audio_processing(duration=3)
        
        # Should return None due to timeout
        assert result is None
        
        client.close()
    
    def test_full_workflow_integration(self):
        """Test a complete workflow from connection to processing"""
        client = AudioServiceClient(server_address=self.server_address)
        
        # Step 1: Health check
        assert client.health_check() is True
        
        # Step 2: Wait for service (should be immediate since it's healthy)
        assert client.wait_for_service(max_retries=1, retry_delay=0.1) is True
        
        # Step 3: Start processing
        processing_result = client.start_audio_processing(duration=5)
        assert processing_result is not None
        assert processing_result['success'] is True
        session_id = processing_result['session_id']
        
        # Step 4: Check status
        status_result = client.get_processing_status(session_id)
        assert status_result is not None
        assert status_result['session_id'] == session_id
        assert status_result['status'] == 'completed'
        
        # Step 5: Close connection
        client.close()
    
    def test_server_unavailable_integration(self):
        """Test behavior when server is unavailable"""
        # Get an address for a server that doesn't exist
        unavailable_address = "localhost:99999"
        
        # Try to connect to non-existent server
        # The connection might succeed initially but fail on actual RPC calls
        client = AudioServiceClient(server_address=unavailable_address)
        
        # The health check should fail when trying to communicate
        result = client.health_check()
        assert result is False
        
        client.close()
    
    def test_concurrent_clients_integration(self):
        """Test multiple concurrent clients"""
        def create_and_test_client():
            client = AudioServiceClient(server_address=self.server_address)
            result = client.start_audio_processing(duration=1)
            client.close()
            return result['success'] if result else False
        
        # Create multiple threads with clients
        threads = []
        results = []
        
        def worker():
            results.append(create_and_test_client())
        
        for _ in range(5):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All clients should succeed
        assert all(results)
        assert len(results) == 5
