"""
Artwork analysis utilities
"""

from PIL import Image

def analyze_artwork(image, model_pipeline):
    """
    Analyze artistic elements in an image
    
    Args:
        image: PIL Image object
        model_pipeline: Loaded transformers pipeline
        
    Returns:
        str: Art analysis or error message
    """
    if image is None:
        return " No image provided"
    
    # Validate image
    try:
        if not isinstance(image, Image.Image):
            return " Invalid image format"
    except Exception as e:
        return f" Image validation error: {str(e)}"
    
    # Create prompt
    prompt = _get_art_analysis_prompt()
    
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
        analysis = output[0]["generated_text"][-1]["content"]
        
        # Post-process
        if not analysis or analysis.strip() == "":
            return " Could not analyze artwork. Try a different image."
        
        return analysis.strip()
        
    except Exception as e:
        return f"Error analyzing artwork: {str(e)}\n\nTip: Ensure the artwork is clearly visible."

def _get_art_analysis_prompt():
    """
    Generate the art analysis prompt for the model
    
    Returns:
        str: Formatted prompt
    """
    return """You are an expert art historian and critic. Analyze any artwork, painting, sketch, or drawing in this image.

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

def get_art_categories():
    """
    Return list of common art styles for reference
    
    Returns:
        dict: Categories of art styles
    """
    return {
        "classical": ["Renaissance", "Baroque", "Neoclassical", "Romanticism"],
        "modern": ["Impressionism", "Post-Impressionism", "Expressionism", "Cubism", "Surrealism"],
        "contemporary": ["Abstract", "Pop Art", "Minimalism", "Contemporary", "Digital Art"],
        "traditional": ["Realism", "Naturalism", "Academic Art"],
        "other": ["Folk Art", "Outsider Art", "Street Art", "Illustration"]
    }

def format_analysis(raw_analysis):
    """
    Format and structure the raw analysis output
    
    Args:
        raw_analysis (str): Raw model output
        
    Returns:
        str: Formatted analysis
    """
    # Basic formatting - can be expanded
    if not raw_analysis:
        return "No analysis available"
    
    # Add any additional formatting here
    formatted = raw_analysis.strip()
    
    return formatted