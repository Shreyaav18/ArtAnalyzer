import gradio as gr
from utils import load_model, extract_handwriting, analyze_artwork

print("Initializing application...")
model_pipeline = load_model(model_name="Salesforce/blip2-opt-2.7b")

def process_image(image):
    """
    Main processing function that coordinates OCR and art analysis
    
    Args:
        image: PIL Image object from Gradio
        
    Returns:
        tuple: (status_message, ocr_result, art_analysis_result)
    """
    if image is None:
        return "Please upload an image", "", ""
    
    status = " Processing... Extracting handwriting..."
    
    handwriting_result = extract_handwriting(image, model_pipeline)
    status = " Processing... Analyzing artwork..."
    art_result = analyze_artwork(image, model_pipeline)
    status = " Analysis complete!"
    
    return status, handwriting_result, art_result

def clear_interface():
    """
    Reset the interface to initial state
    
    Returns:
        tuple: Empty values for all outputs
    """
    return None, "### Status: Waiting for image...", "", ""

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    # Header
    gr.Markdown("""
    # Handwritten Art Notes Analyzer
    
    Upload an image containing handwritten notes and/or artwork. 
    This tool will:
    - **Extract** handwritten text and make it digital
    - **Analyze** any artwork for style, technique, and historical context
    """)
    
    gr.Markdown("---")
    gr.Markdown("###  Upload Your Image")
    
    # Main layout
    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(
                type="pil", 
                label="Upload Image with Handwriting or Artwork",
                height=400
            )
            
            with gr.Row():
                analyze_btn = gr.Button(
                    " Analyze", 
                    variant="primary", 
                    size="lg",
                    scale=2
                )
                clear_btn = gr.Button(
                    " Clear", 
                    size="lg",
                    scale=1
                )

    status_output = gr.Markdown("### Status: Waiting for image...")
    
    gr.Markdown("---")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Extracted Handwriting")
            text_output = gr.Textbox(
                label="Digital Text",
                lines=12,
                placeholder="Handwritten text will appear here...",
                show_copy_button=True
            )
        
        with gr.Column(scale=1):
            gr.Markdown("### Artwork Analysis")
            art_output = gr.Textbox(
                label="Art Analysis",
                lines=12,
                placeholder="Artwork analysis will appear here...",
                show_copy_button=True
            )
    
    analyze_btn.click(
        fn=process_image,
        inputs=[image_input],
        outputs=[status_output, text_output, art_output]
    )
    
    clear_btn.click(
        fn=clear_interface,
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
    
    ### 📊 Current Version: 1.0
    -  Handwriting extraction (OCR)
    -  Art style & technique analysis
    -  Historical context identification
    -  RAG integration (coming in v2.0)
    
    ### 🛠️ Tech Stack:
    - Model: Salesforce BLIP-2
    - Framework: Gradio + Transformers
    - Deployment: Hugging Face Spaces
    """)

if __name__ == "__main__":
    demo.launch(pwa=True, share=True)