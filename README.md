# 🌙 Hippocratic AI Bedtime Story Generator

An **AI-powered interactive bedtime story generator** for children aged 5–10.  
This project uses OpenAI's GPT-4o model to generate short, engaging, safe, and moral-rich stories, with a built-in “judge” to provide feedback and iterative improvements.

---

## Features

- 🎨 **Story Generation**: Generate short bedtime stories with a clear story arc.
- 🧙 **Ethical Story Judge**: Automatically evaluates the story for safety, age-appropriateness, and creativity.
- 🔁 **Iterative Improvement**: Users can give feedback to refine the story.
- 🎲 **Category Selection**: Choose from Adventure, Fantasy, Mystery, Animal Tales, Friendship, or let it pick randomly.
- 🌐 **Web Interface**: Lightweight Gradio-based UI for an interactive browser experience.

---

## Demo

![Demo Screenshot](screenshot.png)  <!-- Optional: add your own screenshot -->

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/<your-username>/hippocratic-bedtime-ai.git
cd hippocratic-bedtime-ai
```
2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create a .env file in the root with your OpenAI API key:
```bash
OPENAI_API_KEY=your_openai_key_here
```