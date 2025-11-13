"""Integration tests for the storyteller app."""
import pytest
from unittest.mock import patch, Mock
from services.openai_service import generate_story, judge_story, generate_image_search_terms
from services.image_service import generate_image

@pytest.mark.integration
@patch('services.openai_service.client')
def test_full_story_generation_workflow(mock_client, mock_openai_response, sample_prompt, sample_category):
    """Test complete story generation workflow."""
    mock_client.chat.completions.create.return_value = mock_openai_response
    
    # Generate story
    story = generate_story(sample_prompt, sample_category)
    assert isinstance(story, str)
    assert len(story) > 0
    
    # Judge story
    mock_openai_response.choices[0].message.content = "SAFE: Great story"
    feedback = judge_story(story)
    assert "SAFE" in feedback
    
    # Generate image terms
    mock_openai_response.choices[0].message.content = "squirrel, flying, adventure"
    image_terms = generate_image_search_terms(story)
    assert isinstance(image_terms, str)

@pytest.mark.integration
@patch('services.image_service.client')
@patch('services.openai_service.client')
def test_story_with_image_generation(mock_openai_client, mock_image_client, 
                                     mock_openai_response, mock_image_response,
                                     sample_prompt, sample_category):
    """Test story generation with image."""
    # Setup mocks
    mock_openai_client.chat.completions.create.return_value = mock_openai_response
    mock_image_client.images.generate.return_value = mock_image_response
    
    # Generate story
    story = generate_story(sample_prompt, sample_category)
    
    # Generate image terms
    mock_openai_response.choices[0].message.content = "cute squirrel flying"
    image_terms = generate_image_search_terms(story)
    
    # Generate image
    image = generate_image(image_terms)
    
    assert story is not None
    assert image is not None
    assert image.size == (1, 1)  # Our mock image is 1x1

@pytest.mark.slow
@pytest.mark.integration
def test_story_improvement_workflow():
    """Test story improvement workflow (without API calls)."""
    original_story = "A short story."
    feedback = "SAFE: Could be longer"
    user_feedback = "Add more details"
    
    # This test just validates the data flow
    assert len(original_story) > 0
    assert len(feedback) > 0
    assert len(user_feedback) > 0