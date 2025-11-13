"""Test TTS service module."""
import pytest
from unittest.mock import patch, MagicMock, Mock
from services.tts_service import TTSService

@pytest.mark.unit
@patch('services.tts_service.pyttsx3')
def test_tts_service_initialization(mock_pyttsx3, mock_tts_engine):
    """Test TTS service initialization."""
    mock_pyttsx3.init.return_value = mock_tts_engine
    
    service = TTSService()
    
    assert service.engine is not None
    assert service.is_reading is False
    mock_pyttsx3.init.assert_called_once()

@pytest.mark.unit
@patch('services.tts_service.pyttsx3')
def test_read_aloud_empty_text(mock_pyttsx3, mock_tts_engine):
    """Test reading empty text."""
    mock_pyttsx3.init.return_value = mock_tts_engine
    service = TTSService()
    
    result = service.read_aloud("")
    
    assert "No story to read" in result
    assert service.is_reading is False

@pytest.mark.unit
@patch('services.tts_service.pyttsx3')
@patch('services.tts_service.threading.Thread')
def test_read_aloud_starts_thread(mock_thread, mock_pyttsx3, mock_tts_engine, sample_story):
    """Test that read_aloud starts a thread."""
    mock_pyttsx3.init.return_value = mock_tts_engine
    mock_thread_instance = MagicMock()
    mock_thread.return_value = mock_thread_instance
    
    service = TTSService()
    result = service.read_aloud(sample_story)
    
    assert "Reading story" in result
    mock_thread_instance.start.assert_called_once()

@pytest.mark.unit
@patch('services.tts_service.pyttsx3')
def test_stop_not_reading(mock_pyttsx3, mock_tts_engine):
    """Test stop when not reading."""
    mock_pyttsx3.init.return_value = mock_tts_engine
    service = TTSService()
    
    result = service.stop()
    
    assert "No story is currently being read" in result

@pytest.mark.unit
@patch('services.tts_service.pyttsx3')
def test_stop_while_reading(mock_pyttsx3, mock_tts_engine):
    """Test stopping while reading."""
    mock_pyttsx3.init.return_value = mock_tts_engine
    service = TTSService()
    service.is_reading = True
    
    result = service.stop()
    
    assert "stopped" in result.lower()
    assert service.is_reading is False
    mock_tts_engine.stop.assert_called_once()

@pytest.mark.unit
@patch('services.tts_service.pyttsx3')
def test_tts_engine_configuration(mock_pyttsx3, mock_tts_engine, sample_story):
    """Test that TTS engine is configured with correct settings."""
    mock_pyttsx3.init.return_value = mock_tts_engine
    
    # Mock voices
    mock_voice1 = Mock()
    mock_voice1.name = "Male Voice"
    mock_voice2 = Mock()
    mock_voice2.name = "Female Voice Zira"
    
    mock_tts_engine.getProperty.return_value = [mock_voice1, mock_voice2]
    
    service = TTSService()
    service.read_aloud(sample_story)
    
    # Give thread time to start
    import time
    time.sleep(0.1)
    
    # Check that properties were set
    assert mock_tts_engine.setProperty.called