from openai import OpenAI
from config import OPENAI_API_KEY, STORY_MODEL, STORY_MAX_TOKENS, STORY_TEMPERATURE, STORY_WORD_COUNT

client = OpenAI(api_key=OPENAI_API_KEY)

def call_model(prompt, max_tokens=STORY_MAX_TOKENS, temperature=STORY_TEMPERATURE):
    """Call OpenAI chat model."""
    return client.chat.completions.create(
        model=STORY_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    ).choices[0].message.content.strip()

def generate_story(user_prompt, category):
    """Generate a children's story."""
    from config import STORY_WORD_COUNT, TARGET_AGE_RANGE
    return call_model(
        f"Write a {STORY_WORD_COUNT}-word imaginative, safe bedtime story for ages {TARGET_AGE_RANGE}.\n"
        f"Category: {category}\nPrompt: {user_prompt}\n\nStory:"
    )

def judge_story(story):
    """Judge story safety and moral clarity."""
    from config import TARGET_AGE_RANGE
    return call_model(
        f"Judge this children's story (ages {TARGET_AGE_RANGE}) for safety, moral clarity, and creativity. "
        "Respond with 'SAFE' or 'NOT SAFE' and one-line suggestion:\n\n" + story,
        temperature=0.3
    )

def generate_image_search_terms(story):
    """Generate search terms for illustration based on story."""
    return call_model(
        f"Give 2–3 short search terms for a children's illustration based on this story:\n{story}",
        50, 0.3
    )

def improve_story_text(story, judge_feedback, user_feedback=""):
    """Improve story based on feedback."""
    return call_model(
        f"Improve this children's story based on judge and reader feedback:\n\n"
        f"Word Count: {STORY_WORD_COUNT}\nStory:\n{story}\n\nJudge:\n{judge_feedback}\nReader:\n{user_feedback}\n\nImproved story:"
    )