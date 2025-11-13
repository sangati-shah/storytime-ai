"""Test OpenAI service module."""
import pytest
from unittest.mock import patch, Mock
from services.openai_service import (
    call_model, generate_story, judge_story,
    generate_image_search_terms, improve_story_text
)

@pytest.mark.unit
@patch('services.openai_service.client')
def test_call_model(mock_client, mock_openai_response):
    """Test basic model call."""
    mock_client.chat.completions.create.return_value = mock_openai_response
    
    result = call_model("Test prompt")
    
    assert result == "Once upon a time in a magical forest..."
    mock_client.chat.completions.create.assert_called_once()

@pytest.mark.unit
@patch('services.openai_service.client')
def test_call_model_with_parameters(mock_client, mock_openai_response):
    """Test model call with custom parameters."""
    mock_client.chat.completions.create.return_value = mock_openai_response
    
    result = call_model("Test prompt", max_tokens=500, temperature=0.5)
    
    call_args = mock_client.chat.completions.create.call_args
    assert call_args[1]['max_tokens'] == 500
    assert call_args[1]['temperature'] == 0.5

@pytest.mark.unit
@patch('services.openai_service.call_model')
def test_generate_story(mock_call_model, sample_prompt, sample_category):
    """Test story generation."""
    mock_call_model.return_value = "A wonderful story about adventure..."
    
    result = generate_story(sample_prompt, sample_category)
    
    assert isinstance(result, str)
    assert len(result) > 0
    mock_call_model.assert_called_once()
    
    # Check that prompt contains category and user prompt
    call_args = mock_call_model.call_args[0][0]
    assert sample_category in call_args
    assert sample_prompt in call_args

@pytest.mark.unit
@patch('services.openai_service.call_model')
def test_judge_story(mock_call_model, sample_story):
    """Test story judging."""
    mock_call_model.return_value = "SAFE: Great story with positive message"
    
    result = judge_story(sample_story)
    
    assert "SAFE" in result
    mock_call_model.assert_called_once()
    
    # Check that story is included in prompt
    call_args = mock_call_model.call_args[0][0]
    assert sample_story in call_args

@pytest.mark.unit
@patch('services.openai_service.call_model')
def test_generate_image_search_terms(mock_call_model, sample_story):
    """Test image search term generation."""
    mock_call_model.return_value = "squirrel, flying, forest"
    
    result = generate_image_search_terms(sample_story)
    
    assert isinstance(result, str)
    assert len(result) > 0
    mock_call_model.assert_called_once()

@pytest.mark.unit
@patch('services.openai_service.call_model')
def test_improve_story_text(mock_call_model, sample_story):
    """Test story improvement."""
    mock_call_model.return_value = "Improved version of the story..."
    
    result = improve_story_text(sample_story, "SAFE", "Add more excitement")
    
    assert isinstance(result, str)
    assert len(result) > 0
    mock_call_model.assert_called_once()
    
    # Check all feedback is included
    call_args = mock_call_model.call_args[0][0]
    assert sample_story in call_args
    assert "SAFE" in call_args
    assert "Add more excitement" in call_args

@pytest.mark.unit
@patch('services.openai_service.client')
def test_call_model_error_handling(mock_client):
    """Test error handling in model calls."""
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    
    with pytest.raises(Exception) as exc_info:
        call_model("Test prompt")
    
    assert "API Error" in str(exc_info.value)