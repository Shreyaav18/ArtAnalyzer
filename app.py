import os
import gradio as gr
from transformers import pipeline
import torch
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

print("Loading model... This may take a minute...")
pipe = pipeline(
    "image-text-to-text",
    model="Salesforce/blip2-opt-2.7b",  # Good for both OCR and visual tasks
    token=hf_token,
    device="cuda" if torch.cuda.is_available() else "cpu",
    torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
)
print("Model loaded successfully!")

def extract_handwriting(image):
    """
    Extract handwritten text from the image
    """
    if image is None:
        return "No image provided"
    
    prompt = """You are an expert OCR system specializing in handwritten text recognition.

Task: Extract ALL handwritten text from this image.

Instructions:
- Transcribe exactly what is written, word for word
- Preserve line breaks and paragraph structure
- Include any crossed-out text in [strikethrough: text] format
- If text is unclear, use [unclear: best_guess] format
- Ignore any printed text, focus only on handwriting
- If no handwriting exists, respond with: "No handwritten text detected"

Output the transcribed text directly without explanations."""
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt}
            ]
        }
    ]
    
    try:
        output = pipe(messages, max_new_tokens=500)
        extracted_text = output[0]["generated_text"][-1]["content"]
        if not extracted_text or extracted_text.strip() == "":
            return "No text could be extracted. Try a clearer image."
        
        return extracted_text.strip()

    except Exception as e:
        return f"Error extracting text: {str(e)}"

def analyze_artwork(image):
    """
    Analyze the artistic elements in the image
    """
    if image is None:
        return "No image provided"
    
    prompt = """You are an expert art historian and critic. Analyze any artwork, painting, sketch, or drawing in this image.

Provide a detailed analysis in the following structure:

**Art Style & Movement:**
Identify the artistic style (e.g., Renaissance, Impressionism, Cubism, Abstract, Contemporary, etc.)

**Medium & Technique:**
Describe the medium used (oil, watercolor, pencil, charcoal, digital, etc.) and technical approach

**Subject & Composition:**
What is depicted? How is the composition arranged?

**Visual Elements:**
- Color palette and use of color
- Light and shadow
- Perspective and depth
- Texture and brushwork (if visible)

**Historical & Cultural Context:**
Time period, art movement, or cultural significance (if identifiable)

**Notable Characteristics:**
Unique features, symbolism, or artistic choices

If no artwork is visible, respond with: "No artwork detected in this image"

Provide your analysis in clear paragraphs."""
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt}
            ]
        }
    ]
    
    try:
        output = pipe(messages, max_new_tokens=500)
        analysis = output[0]["generated_text"][-1]["content"]
        if not analysis or analysis.strip() == "":
            return "Could not analyze artwork. Try a different image."
        
        return analysis.strip()
    except Exception as e:
        return f" Error analyzing artwork: {str(e)}"

def process_image(image):
    """
    Main function that combines both OCR and art analysis
    """
    if image is None:
        return " Please upload an image", "", ""
    
    # Run both analyses
    status = "Processing complete!"
    handwriting_result = extract_handwriting(image)
    art_result = analyze_artwork(image)
    
    return status, handwriting_result, art_result

# Create Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎨✍️ Handwritten Art Notes Analyzer
    
    Upload an image containing handwritten notes and/or artwork. 
    This tool will:
    - **Extract** handwritten text and make it digital
    - **Analyze** any artwork for style, technique, and historical context
    """)
    
    gr.Markdown("### 📸 Upload Your Image")
    
    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(
                type="pil", 
                label="Upload Image with Handwriting or Artwork",
                height=400
            )
            analyze_btn = gr.Button("🔍 Analyze", variant="primary", size="lg")
            clear_btn = gr.Button("🗑️ Clear", size="lg")
    
    status_output = gr.Markdown("### Status: Waiting for image...")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Extracted Handwriting")
            text_output = gr.Textbox(
                label="Digital Text",
                lines=10,
                placeholder="Handwritten text will appear here..."
            )
        
        with gr.Column(scale=1):
            gr.Markdown("### 🎨 Artwork Analysis")
            art_output = gr.Textbox(
                label="Art Analysis",
                lines=10,
                placeholder="Artwork analysis will appear here..."
            )
    
    # Button actions
    analyze_btn.click(
        fn=process_image,
        inputs=[image_input],
        outputs=[status_output, text_output, art_output]
    )
    
    clear_btn.click(
        fn=lambda: (None, "### Status: Waiting for image...", "", ""),
        inputs=[],
        outputs=[image_input, status_output, text_output, art_output]
    )
    
    gr.Markdown("""
    ---
    ### 💡 Tips for Best Results:
    - Use clear, well-lit images
    - Ensure handwriting is legible
    - Higher resolution images work better
    - Try different angles if results aren't satisfactory
    
    ### 🚀 Version 1.0 (Without RAG)
    Future updates will include RAG for deeper art history knowledge!
    """)

if __name__ == "__main__":
    demo.launch(pwa=True,share=True)