"""Test configuration module."""
import pytest
from config import (
    OPENAI_API_KEY, STORY_MODEL, IMAGE_MODEL,
    STORY_MAX_TOKENS, STORY_CATEGORIES, PLACEHOLDER_SIZE
)

@pytest.mark.unit
def test_api_key_loaded():
    """Test that API key is loaded."""
    assert OPENAI_API_KEY is not None
    assert len(OPENAI_API_KEY) > 0

@pytest.mark.unit
def test_model_configuration():
    """Test model configuration values."""
    assert STORY_MODEL == "gpt-4o"
    assert IMAGE_MODEL == "gpt-image-1"

@pytest.mark.unit
def test_story_settings():
    """Test story configuration settings."""
    assert STORY_MAX_TOKENS == 800
    assert isinstance(STORY_MAX_TOKENS, int)
    assert STORY_MAX_TOKENS > 0

@pytest.mark.unit
def test_categories_exist():
    """Test that story categories are defined."""
    assert len(STORY_CATEGORIES) > 0
    assert "Adventure" in STORY_CATEGORIES
    assert "Random" in STORY_CATEGORIES

@pytest.mark.unit
def test_placeholder_image_settings():
    """Test placeholder image configuration."""
    assert PLACEHOLDER_SIZE == (600, 400)
    assert isinstance(PLACEHOLDER_SIZE, tuple)
    assert len(PLACEHOLDER_SIZE) == 2