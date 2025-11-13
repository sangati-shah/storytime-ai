import base64
import io
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
from config import (
    OPENAI_API_KEY, IMAGE_MODEL, IMAGE_SIZE,
    PLACEHOLDER_SIZE, PLACEHOLDER_BG_COLOR, PLACEHOLDER_TEXT_COLOR
)

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_placeholder_image(text="🎨 Generating your illustration..."):
    """Return a simple PIL placeholder image."""
    img = Image.new("RGB", PLACEHOLDER_SIZE, color=PLACEHOLDER_BG_COLOR)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    bbox = d.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((PLACEHOLDER_SIZE[0] - w) / 2, (PLACEHOLDER_SIZE[1] - h) / 2), 
           text, fill=PLACEHOLDER_TEXT_COLOR, font=font)
    return img

def generate_image(query):
    """Generate image synchronously."""
    try:
        img_resp = client.images.generate(
            model=IMAGE_MODEL,
            prompt=f"A cute, safe children's illustration for: {query}",
            size=IMAGE_SIZE
        )
        
        # Convert base64 to PIL Image
        image_base64 = img_resp.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        img = Image.open(io.BytesIO(image_bytes))
        return img
        
    except Exception as e:
        print(f"Image generation failed: {e}")
        return generate_placeholder_image("❌ Image generation failed")