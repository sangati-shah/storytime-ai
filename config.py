import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model Settings
STORY_MODEL = "gpt-4o"
IMAGE_MODEL = "gpt-image-1"

# Story Settings
STORY_MAX_TOKENS = 800
STORY_TEMPERATURE = 0.7
STORY_WORD_COUNT = 250
TARGET_AGE_RANGE = "5–10"

# Image Settings
IMAGE_SIZE = "auto"
PLACEHOLDER_SIZE = (600, 400)
PLACEHOLDER_BG_COLOR = (224, 242, 254)
PLACEHOLDER_TEXT_COLOR = (2, 132, 199)

# TTS Settings
TTS_RATE = 150
TTS_VOLUME = 1.0

# Categories
STORY_CATEGORIES = ["Adventure", "Fantasy", "Mystery", "Animal Tales", "Friendship", "Random"]