import gradio as gr
from utils.export_handler import export_to_txt, export_to_json, export_to_pdf, get_filename
from utils.history_manager import HistoryManager
from utils import load_model, extract_handwriting, analyze_artwork

print("Initializing application...")
model_pipeline = load_model(model_name="Salesforce/blip2-opt-2.7b")
history_manager = HistoryManager(max_items=10)

def process_image(image):
    """
    Main processing function that coordinates OCR and art analysis
    
    Args:
        image: PIL Image object from Gradio
        
    Returns:
        tuple: (status_message, ocr_result, art_analysis_result)
    """
    if image is None:
        return "Please upload an image", "", "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), ""
    
    status = "Processing... Extracting handwriting..."
    handwriting_result = extract_handwriting(image, model_pipeline)
    
    status = "Processing... Analyzing artwork..."
    art_result = analyze_artwork(image, model_pipeline)
    
    history_manager.add_entry(image, handwriting_result, art_result)
    
    status = "Analysis complete"
    history_summary = format_history_summary()
    
    return (
        status, 
        handwriting_result, 
        art_result, 
        gr.update(visible=True), 
        gr.update(visible=True), 
        gr.update(visible=True), 
        history_summary
    )

def export_results(format_type, ocr_text, art_text):
    if not ocr_text and not art_text:
        return None
    
    filename = get_filename(format_type)
    
    if format_type == "txt":
        content = export_to_txt(ocr_text, art_text)
        return gr.File.update(value=content.encode(), visible=True)
    elif format_type == "json":
        content = export_to_json(ocr_text, art_text)
        return gr.File.update(value=content.encode(), visible=True)
    elif format_type == "pdf":
        content = export_to_pdf(ocr_text, art_text)
        return gr.File.update(value=content, visible=True)

def format_history_summary():
    summary = history_manager.get_summary()
    if not summary:
        return "No history available"
    
    formatted = "Recent Analyses:\n\n"
    for item in reversed(summary):
        formatted += f"{item['index']}. {item['timestamp']}\n"
        formatted += f"   OCR: {item['ocr_preview']}\n"
        formatted += f"   Art: {item['art_preview']}\n\n"
    return formatted

def load_history_entry(history_index):
    if history_index is None:
        return None, "", ""
    
    entry = history_manager.get_entry(int(history_index) - 1)
    if entry:
        return entry['image'], entry['ocr_result'], entry['art_result']
    return None, "", ""

def clear_all_history():
    history_manager.clear_history()
    return "History cleared", ""

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
    
    gr.Markdown("---")
    gr.Markdown("### Export Results")
    
    with gr.Row():
        export_txt_btn = gr.Button("Export as TXT", visible=False)
        export_json_btn = gr.Button("Export as JSON", visible=False)
        export_pdf_btn = gr.Button("Export as PDF", visible=False)
    
    export_output = gr.File(label="Download", visible=False)
    
    gr.Markdown("---")
    gr.Markdown("### History")
    
    with gr.Row():
        with gr.Column(scale=2):
            history_display = gr.Textbox(
                label="Session History",
                lines=8,
                interactive=False,
                value="No history available"
            )
        with gr.Column(scale=1):
            history_index = gr.Number(
                label="Load Entry (by number)",
                precision=0,
                minimum=1
            )
            load_history_btn = gr.Button("Load from History")
            clear_history_btn = gr.Button("Clear History")
            
    analyze_btn.click(
        fn=process_image,
        inputs=[image_input],
        outputs=[status_output, text_output, art_output, export_txt_btn, export_json_btn, export_pdf_btn, history_display]
    )
    
    clear_btn.click(
        fn=clear_interface,
        inputs=[],
        outputs=[image_input, status_output, text_output, art_output, export_txt_btn, export_json_btn, export_pdf_btn, history_display]
    )
    
    export_txt_btn.click(
        fn=lambda ocr, art: export_results("txt", ocr, art),
        inputs=[text_output, art_output],
        outputs=[export_output]
    )
    
    export_json_btn.click(
        fn=lambda ocr, art: export_results("json", ocr, art),
        inputs=[text_output, art_output],
        outputs=[export_output]
    )
    
    export_pdf_btn.click(
        fn=lambda ocr, art: export_results("pdf", ocr, art),
        inputs=[text_output, art_output],
        outputs=[export_output]
    )
    
    load_history_btn.click(
        fn=load_history_entry,
        inputs=[history_index],
        outputs=[image_input, text_output, art_output]
    )
    
    clear_history_btn.click(
        fn=clear_all_history,
        inputs=[],
        outputs=[status_output, history_display]
    )

    gr.Markdown("""
    ---
    ### Tips for Best Results:
    - Use clear, well-lit images
    - Ensure handwriting is legible
    - Higher resolution images work better
    - Try different angles if results aren't satisfactory
    
    ### Current Version: 1.0
    -  Handwriting extraction (OCR)
    -  Art style & technique analysis
    -  Historical context identification
    -  RAG integration (coming in v2.0)
    
    ### Tech Stack:
    - Model: Salesforce BLIP-2
    - Framework: Gradio + Transformers
    - Deployment: Hugging Face Spaces
    """)

if __name__ == "__main__":
    demo.launch(pwa=True, share=True)