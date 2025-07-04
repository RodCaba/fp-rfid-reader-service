import pytest
from unittest.mock import Mock, patch
import os
from src.audio_client import AudioServiceClient

@patch('src.audio_client.audio_service_pb2_grpc.AudioServiceStub')
@patch('src.audio_client.grpc.insecure_channel')
class TestAudioServiceClient:
  """
  Tests the gRPC AudioServiceClient class.
  This test class verifies the functionality of the AudioServiceClient class by mocking
  the gRPC channel and stub, and validating:
  - Proper initialization with default and custom server addresses
  - Connection handling
  - Health check functionality
  - Service availability checks
  - Audio processing start and status retrieval
  - Error handling during audio processing
  """
  
  def test_init_default_address(self, mock_channel, mock_stub):
    """Test initialization with default server address"""
    client = AudioServiceClient()
    
    mock_channel.assert_called_once_with('localhost:50051')
    mock_stub.assert_called_once_with(mock_channel.return_value)
    assert client.server_address == 'localhost:50051'
    assert client.timeout == 30
  
  def test_init_custom_address(self, mock_channel, mock_stub):
    """Test initialization with custom server address"""
    client = AudioServiceClient(server_address='custom:8080', timeout=60)
    
    mock_channel.assert_called_once_with('custom:8080')
    assert client.server_address == 'custom:8080'
    assert client.timeout == 60
  
  @patch.dict(os.environ, {'AUDIO_SERVICE_URL': 'env:9090'})
  def test_init_env_address(self, mock_channel, mock_stub):
    """Test initialization with environment variable address"""
    client = AudioServiceClient()
    
    mock_channel.assert_called_once_with('env:9090')
    assert client.server_address == 'env:9090'
  
  def test_connect_failure(self, mock_channel, mock_stub):
    """Test connection failure handling"""
    mock_channel.side_effect = Exception("Connection failed")
    
    with pytest.raises(Exception, match="Connection failed"):
      AudioServiceClient()
  
  def test_health_check_success(self, mock_channel, mock_stub):
    """Test successful health check"""
    client = AudioServiceClient()
    
    mock_response = Mock()
    mock_response.status = "SERVING"
    client.stub.HealthCheck.return_value = mock_response
    
    result = client.health_check()
    
    assert result is True
    client.stub.HealthCheck.assert_called_once()
  
  def test_health_check_failure(self, mock_channel, mock_stub):
    """Test health check failure"""
    client = AudioServiceClient()
    
    client.stub.HealthCheck.side_effect = Exception("gRPC error")
    
    result = client.health_check()
    
    assert result is False
  
  @patch('src.audio_client.time.sleep')
  def test_wait_for_service_success(self, mock_sleep, mock_channel, mock_stub):
    """Test waiting for service to become available"""
    client = AudioServiceClient()
    
    mock_response = Mock()
    mock_response.status = "SERVING"
    client.stub.HealthCheck.return_value = mock_response
    
    result = client.wait_for_service(max_retries=3, retry_delay=1)
    
    assert result is True
    client.stub.HealthCheck.assert_called()
  
  @patch('src.audio_client.time.sleep')
  def test_wait_for_service_timeout(self, mock_sleep, mock_channel, mock_stub):
    """Test waiting for service timeout"""
    client = AudioServiceClient()
    
    client.stub.HealthCheck.side_effect = Exception("Service unavailable")
    
    result = client.wait_for_service(max_retries=2, retry_delay=1)
    
    assert result is False
    assert client.stub.HealthCheck.call_count == 2
    assert mock_sleep.call_count == 2
  
  @patch('src.audio_client.uuid.uuid4')
  def test_start_audio_processing_success(self, mock_uuid, mock_channel, mock_stub):
    """Test successful audio processing start"""
    client = AudioServiceClient()
    mock_uuid.return_value = Mock()
    mock_uuid.return_value.__str__ = Mock(return_value="test-session-id")
    
    # Mock response
    mock_prediction = Mock()
    mock_prediction.class_name = "test_class"
    mock_prediction.probability = 0.95
    
    mock_response = Mock()
    mock_response.success = True
    mock_response.session_id = "test-session-id"
    mock_response.predicted_class = "test_class"
    mock_response.confidence = 0.95
    mock_response.top_predictions = [mock_prediction]
    
    client.stub.StartAudioProcessing.return_value = mock_response
    
    result = client.start_audio_processing(duration=10)
    
    assert result['success'] is True
    assert result['session_id'] == "test-session-id"
    assert result['predicted_class'] == "test_class"
    assert result['confidence'] == 0.95
    assert len(result['top_predictions']) == 1
    assert result['top_predictions'][0]['class_name'] == "test_class"
    assert result['top_predictions'][0]['probability'] == 0.95
  
  def test_start_audio_processing_failure(self, mock_channel, mock_stub):
    """Test audio processing start failure"""
    client = AudioServiceClient()
    
    mock_response = Mock()
    mock_response.success = False
    mock_response.session_id = "test-session-id"
    mock_response.error_message = "Processing failed"
    
    client.stub.StartAudioProcessing.return_value = mock_response
    
    result = client.start_audio_processing(session_id="test-session-id")
    
    assert result['success'] is False
    assert result['session_id'] == "test-session-id"
    assert result['error_message'] == "Processing failed"
  
  def test_start_audio_processing_exception(self, mock_channel, mock_stub):
    """Test audio processing start with exception"""
    client = AudioServiceClient()
    
    client.stub.StartAudioProcessing.side_effect = Exception("gRPC error")
    
    result = client.start_audio_processing()
    
    assert result is None
  
  def test_get_processing_status_success(self, mock_channel, mock_stub):
    """Test successful processing status retrieval"""
    client = AudioServiceClient()
    
    mock_response = Mock()
    mock_response.session_id = "test-session-id"
    mock_response.status = "PROCESSING"
    mock_response.current_operation = "RECORDING"
    
    client.stub.GetProcessingStatus.return_value = mock_response
    
    result = client.get_processing_status("test-session-id")
    
    assert result['session_id'] == "test-session-id"
    assert result['status'] == "PROCESSING"
    assert result['current_operation'] == "RECORDING"
  
  def test_get_processing_status_exception(self, mock_channel, mock_stub):
    """Test processing status retrieval with exception"""
    client = AudioServiceClient()
    
    client.stub.GetProcessingStatus.side_effect = Exception("gRPC error")
    
    result = client.get_processing_status("test-session-id")
    
    assert result is None
  
  def test_close(self, mock_channel, mock_stub):
    """Test closing the connection"""
    client = AudioServiceClient()
    
    client.close()
    
    client.channel.close.assert_called_once()