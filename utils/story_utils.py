import random
from config import STORY_CATEGORIES

def get_random_category():
    """Get a random story category."""
    return random.choice([c for c in STORY_CATEGORIES if c != "Random"])

def validate_story_prompt(prompt):
    """Validate that the story prompt is not empty."""
    return bool(prompt and prompt.strip())