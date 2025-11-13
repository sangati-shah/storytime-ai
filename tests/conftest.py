"""Pytest configuration and shared fixtures."""
import pytest
import os
from unittest.mock import Mock, MagicMock
from PIL import Image

# Set test environment
os.environ['OPENAI_API_KEY'] = 'test-key-12345'

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Once upon a time in a magical forest..."
    return mock_response

@pytest.fixture
def mock_image_response():
    """Mock OpenAI image generation response."""
    mock_response = Mock()
    mock_response.data = [Mock()]
    # Base64 encoded 1x1 red pixel PNG
    mock_response.data[0].b64_json = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="
    )
    return mock_response

@pytest.fixture
def sample_story():
    """Sample story text for testing."""
    return """Once upon a time, in a cozy burrow beneath a big oak tree, 
    lived a brave little squirrel named Squeaky. Squeaky had a dream that 
    seemed impossible: he wanted to fly like the birds he saw every day."""

@pytest.fixture
def sample_category():
    """Sample story category."""
    return "Adventure"

@pytest.fixture
def sample_prompt():
    """Sample story prompt."""
    return "A brave squirrel who wants to fly"

@pytest.fixture
def mock_pil_image():
    """Create a mock PIL Image."""
    return Image.new("RGB", (100, 100), color="red")

@pytest.fixture
def mock_tts_engine():
    """Mock pyttsx3 TTS engine."""
    mock_engine = MagicMock()
    mock_engine.getProperty.return_value = []
    mock_engine.setProperty.return_value = None
    mock_engine.say.return_value = None
    mock_engine.startLoop.return_value = None
    mock_engine.endLoop.return_value = None
    mock_engine.stop.return_value = None
    mock_engine.isBusy.return_value = False
    return mock_engine