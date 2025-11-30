"""
Handwriting OCR extraction utilities
"""

from PIL import Image

def extract_handwriting(image, model_pipeline):
    """
    Extract handwritten text from an image
    
    Args:
        image: PIL Image object
        model_pipeline: Loaded transformers pipeline
        
    Returns:
        str: Extracted text or error message
    """
    if image is None:
        return " No image provided"
    
    # Validate image
    try:
        if not isinstance(image, Image.Image):
            return "Invalid image format"
    except Exception as e:
        return f"Image validation error: {str(e)}"
    
    # Create prompt
    prompt = _get_ocr_prompt()
    
    # Build messages
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt}
            ]
        }
    ]
    
    # Process with model
    try:
        output = model_pipeline(messages, max_new_tokens=500)
        extracted_text = output[0]["generated_text"][-1]["content"]
        
        # Post-process the output
        if not extracted_text or extracted_text.strip() == "":
            return " No text could be extracted. Try a clearer image."
        
        return extracted_text.strip()
        
    except Exception as e:
        return f"Error extracting text: {str(e)}\n\nTip: Ensure the image is clear and well-lit."

def _get_ocr_prompt():
    """
    Generate the OCR prompt for the model
    
    Returns:
        str: Formatted prompt
    """
    return """You are an expert OCR system specializing in handwritten text recognition.

Task: Extract ALL handwritten text from this image.

Instructions:
- Transcribe exactly what is written, word for word
- Preserve line breaks and paragraph structure
- Include any crossed-out text in [strikethrough: text] format
- If text is unclear, use [unclear: best_guess] format
- Ignore any printed text, focus only on handwriting
- If no handwriting exists, respond with: "No handwritten text detected"

Output the transcribed text directly without explanations."""

def validate_ocr_output(text):
    """
    Validate and clean OCR output
    
    Args:
        text (str): Raw OCR output
        
    Returns:
        dict: Contains 'valid' (bool) and 'cleaned_text' (str)
    """
    if not text or len(text.strip()) < 3:
        return {
            'valid': False,
            'cleaned_text': text,
            'message': 'Output too short'
        }
    
    cleaned = text.strip()
    
    return {
        'valid': True,
        'cleaned_text': cleaned,
        'message': 'Valid output'
    }