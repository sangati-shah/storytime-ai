import gradio as gr
from config import STORY_CATEGORIES
from services.openai_service import (
    generate_story, judge_story, 
    generate_image_search_terms, improve_story_text
)
from services.image_service import generate_placeholder_image, generate_image
from services.tts_service import tts_service
from utils.story_utils import get_random_category

# ---------- Story Functions ----------
def create_story(user_prompt, category):
    """Generate story (fast) - returns placeholder image."""
    story = generate_story(user_prompt, category)
    feedback = judge_story(story)
    image_terms = generate_image_search_terms(story)
    placeholder = generate_placeholder_image()
    return story, placeholder, feedback, image_terms

def create_story_image(image_terms):
    """Generate the actual image (slow)."""
    if image_terms:
        return generate_image(image_terms)
    return generate_placeholder_image()

def improve_story(story, judge_fb, user_fb=""):
    """Improve story based on feedback."""
    improved_story = improve_story_text(story, judge_fb, user_fb)
    improved_judge_fb = judge_story(improved_story)
    return improved_story, improved_judge_fb

# ---------- Gradio UI ----------
with gr.Blocks(theme=gr.themes.Soft(), css=".center{text-align:center;}") as demo:
    gr.Markdown("# 🌙 Hippocratic Storyteller", elem_classes="center")
    gr.Markdown("### Create magical bedtime stories for children", elem_classes="center")

    loading_text = gr.Markdown("", elem_classes="center")

    with gr.Row(elem_classes="center"):
        cat = gr.Dropdown(
            STORY_CATEGORIES,
            label="Category", 
            value="Adventure"
        )
        prompt = gr.Textbox(
            label="Story Prompt", 
            placeholder="e.g. A brave squirrel who wants to fly"
        )

    gen_btn = gr.Button("✨ Generate Story", variant="primary")

    with gr.Column(visible=False) as story_ui:
        img = gr.Image(label="Illustration", type="pil")
        story = gr.Textbox(label="📖 Your Story", lines=12)
        judge_fb = gr.Textbox(label="✅ Judge Feedback", lines=3)
        user_fb = gr.Textbox(
            label="Your Suggestions", 
            placeholder="e.g. Add a dragon, make it funnier"
        )

        with gr.Row():
            improve_btn = gr.Button("📝 Improve Story")
            read_btn = gr.Button("🔊 Read Story", variant="secondary")
            stop_btn = gr.Button("🛑 Stop Reading", variant="secondary")

        read_status = gr.Textbox(label="", visible=False)

    image_terms_state = gr.State()

    # ---------- Event Handlers ----------
    def generate_story_fast(cat_val, prompt_val):
        """Generate story quickly with placeholder image."""
        cat_val = get_random_category() if cat_val == "Random" else cat_val
        story_text, placeholder_img, judge_fb, img_terms = create_story(prompt_val, cat_val)
        return "", placeholder_img, story_text, judge_fb, gr.update(visible=True), img_terms

    def show_loading():
        return (
            "✍️ Writing your story, please wait...", 
            generate_placeholder_image(), 
            "", "", 
            gr.update(visible=False), 
            ""
        )

    gen_btn.click(
        fn=show_loading,
        inputs=[],
        outputs=[loading_text, img, story, judge_fb, story_ui, image_terms_state]
    ).then(
        fn=generate_story_fast,
        inputs=[cat, prompt],
        outputs=[loading_text, img, story, judge_fb, story_ui, image_terms_state]
    ).then(
        fn=create_story_image,
        inputs=[image_terms_state],
        outputs=[img]
    )

    improve_btn.click(improve_story, [story, judge_fb, user_fb], [story, judge_fb])
    read_btn.click(tts_service.read_aloud, [story], [read_status])
    stop_btn.click(tts_service.stop, [], [read_status])

if __name__ == "__main__":
    demo.launch()