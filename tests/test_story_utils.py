"""Test story utilities module."""
import pytest
from utils.story_utils import get_random_category, validate_story_prompt

@pytest.mark.unit
def test_get_random_category():
    """Test random category generation."""
    category = get_random_category()
    
    assert isinstance(category, str)
    assert len(category) > 0
    assert category != "Random"

@pytest.mark.unit
def test_get_random_category_multiple_calls():
    """Test that random category can vary."""
    categories = set()
    for _ in range(20):
        categories.add(get_random_category())
    
    # Should get at least 2 different categories in 20 tries
    assert len(categories) >= 2

@pytest.mark.unit
def test_validate_story_prompt_valid():
    """Test validation with valid prompt."""
    assert validate_story_prompt("A brave squirrel") is True

@pytest.mark.unit
def test_validate_story_prompt_empty():
    """Test validation with empty prompt."""
    assert validate_story_prompt("") is False
    assert validate_story_prompt("   ") is False

@pytest.mark.unit
def test_validate_story_prompt_none():
    """Test validation with None."""
    assert validate_story_prompt(None) is False