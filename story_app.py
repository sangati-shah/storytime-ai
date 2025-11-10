# story_app.py
import os
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def call_model(prompt: str, max_tokens=1000, temperature=0.7) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return completion.choices[0].message.content

def storyteller(user_prompt: str, category: str) -> str:
    story_prompt = (
        f"You are a warm, imaginative storyteller who writes bedtime stories "
        f"for children aged 5 to 10. The story should be safe, engaging, and have a clear moral. "
        f"Ensure the story follows a clear story arc with a beginning, middle, and end. "
        f"The story should be around 150 words.\n"
        f"Category: {category}\n"
        f"User request: {user_prompt}\n\nNow tell the story:"
    )
    return call_model(story_prompt)

def judge_story(story: str) -> str:
    judge_prompt = (
        "You are an ethical story critic evaluating a bedtime story for children aged 5–10.\n"
        "Please review the story on these dimensions: "
        " - Age Appropriateness\n"
        " - Creativity\n"
        " - Moral Clarity\n"
        " - Vocabulary\n"
        " - Safety & Sensitivity\n\n"
        "Respond with 'SAFE' or 'NOT SAFE' and one short suggestion.\n\n"
        f"Story:\n{story}"
    )
    return call_model(judge_prompt, temperature=0.3)

def improve_story(story: str, feedback: str, user_feedback: str = "") -> str:
    refine_prompt = (
        "You are a helpful editor improving a children’s story based on feedback.\n\n"
        f"Original story:\n{story}\n\n"
        f"Judge feedback:\n{feedback}\n\n"
        f"Reader feedback:\n{user_feedback}\n\n"
        "Improved story:"
    )
    return call_model(refine_prompt)

def random_category():
    categories = ["Adventure", "Fantasy", "Mystery", "Animal Tales", "Friendship"]
    return random.choice(categories)

# only launch Gradio UI if run directly
if __name__ == "__main__":
    import gradio as gr

    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("## 🌙 Hippocratic Storyteller")

        with gr.Row():
            category = gr.Dropdown(
                ["Adventure", "Fantasy", "Mystery", "Animal Tales", "Friendship", "Random"],
                label="Choose a Story Category", value="Adventure"
            )
            request = gr.Textbox(label="Story Prompt", placeholder="e.g. A brave squirrel who wants to fly", lines=1)

        generate_btn = gr.Button("✨ Generate Story")
        story_output = gr.Textbox(label="Story", lines=10)
        judge_output = gr.Textbox(label="Judge Feedback", lines=2)

        with gr.Row():
            user_feedback = gr.Textbox(label="Improvements?", placeholder="e.g. Add a dragon", lines=1)
            improve_btn = gr.Button("📝 Improve Story")

        generate_btn.click(
            lambda cat, req: (
                storyteller(req, random_category() if cat == "Random" else cat),
                judge_story("placeholder")  # simplified for example
            ),
            inputs=[category, request],
            outputs=[story_output, judge_output]
        )

        improve_btn.click(
            lambda story, fb, uf: improve_story(story, fb, uf),
            inputs=[story_output, judge_output, user_feedback],
            outputs=[story_output]
        )

    demo.launch()
