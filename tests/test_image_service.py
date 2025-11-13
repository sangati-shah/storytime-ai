"""Test image service module."""
import pytest
from unittest.mock import patch, Mock
from PIL import Image
from services.image_service import (
    generate_placeholder_image, generate_image
)

@pytest.mark.unit
def test_generate_placeholder_image_default():
    """Test placeholder image generation with default text."""
    img = generate_placeholder_image()
    
    assert isinstance(img, Image.Image)
    assert img.size == (600, 400)
    assert img.mode == "RGB"

@pytest.mark.unit
def test_generate_placeholder_image_custom_text():
    """Test placeholder image with custom text."""
    custom_text = "Custom placeholder text"
    img = generate_placeholder_image(custom_text)
    
    assert isinstance(img, Image.Image)
    assert img.size == (600, 400)

@pytest.mark.unit
@patch('services.image_service.client')
def test_generate_image_success(mock_client, mock_image_response):
    """Test successful image generation."""
    mock_client.images.generate.return_value = mock_image_response
    
    result = generate_image("cute squirrel")
    
    assert isinstance(result, Image.Image)
    mock_client.images.generate.assert_called_once()
    
    # Check that prompt contains the query
    call_args = mock_client.images.generate.call_args
    assert "cute squirrel" in call_args[1]['prompt']

@pytest.mark.unit
@patch('services.image_service.client')
def test_generate_image_failure(mock_client):
    """Test image generation failure fallback."""
    mock_client.images.generate.side_effect = Exception("Image API Error")
    
    result = generate_image("test query")
    
    # Should return placeholder on error
    assert isinstance(result, Image.Image)
    assert result.size == (600, 400)

@pytest.mark.unit
@patch('services.image_service.client')
def test_generate_image_prompt_format(mock_client, mock_image_response):
    """Test that image prompt is properly formatted."""
    mock_client.images.generate.return_value = mock_image_response
    
    generate_image("brave squirrel flying")
    
    call_args = mock_client.images.generate.call_args[1]
    prompt = call_args['prompt']
    
    assert "cute" in prompt.lower()
    assert "safe" in prompt.lower()
    assert "children's illustration" in prompt.lower() or "illustration" in prompt.lower()
    assert "brave squirrel flying" in prompt