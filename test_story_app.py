# test_story_app.py
import pytest
from unittest.mock import patch
import story_app

# --- Mock the call_model function ---
@pytest.fixture
def mock_call_model():
    with patch("story_app.call_model") as mock:
        mock.return_value = "Mocked response"
        yield mock

def test_storyteller_prompt(mock_call_model):
    response = story_app.storyteller("a cat who learns to dance", "Animal Tales")
    assert response == "Mocked response"
    mock_call_model.assert_called_once()
    prompt = mock_call_model.call_args[0][0]
    assert "Animal Tales" in prompt
    assert "a cat who learns to dance" in prompt

def test_judge_story(mock_call_model):
    story = "Once upon a time..."
    response = story_app.judge_story(story)
    assert response == "Mocked response"
    prompt = mock_call_model.call_args[0][0]
    assert "Once upon a time" in prompt
    assert "SAFE" in prompt or "NOT SAFE" in prompt or "Story" in prompt  # checks structure

def test_improve_story(mock_call_model):
    story = "A happy fox who helps friends."
    feedback = "SAFE for children."
    user_feedback = "Add a dragon."
    response = story_app.improve_story(story, feedback, user_feedback)
    assert response == "Mocked response"
    prompt = mock_call_model.call_args[0][0]
    assert "Original story" in prompt
    assert "Add a dragon" in prompt

def test_random_category():
    cats = [story_app.random_category() for _ in range(100)]
    valid = {"Adventure", "Fantasy", "Mystery", "Animal Tales", "Friendship"}
    assert all(c in valid for c in cats)
