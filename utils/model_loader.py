"""
Model loading and initialization utilities
"""

import os
import torch
from transformers import pipeline
from dotenv import load_dotenv

def load_model(model_name="Salesforce/blip2-opt-2.7b"):
    """
    Load and initialize the vision-language model
    
    Args:
        model_name (str): HuggingFace model identifier
        
    Returns:
        pipeline: Initialized transformers pipeline
    """
    # Load environment variables
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")
    
    print(f"Loading model: {model_name}...")
    print("This may take a minute on first run...")
    
    try:
        # Determine device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        
        print(f"Using device: {device}")
        
        # Load pipeline
        pipe = pipeline(
            "image-text-to-text",
            model=model_name,
            token=hf_token,
            device=device,
            torch_dtype=dtype,
        )
        
        print(" Model loaded successfully!")
        return pipe
        
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

def get_available_models():
    """
    Return list of recommended models for this task
    """
    return {
        "blip2": "Salesforce/blip2-opt-2.7b",
        "paligemma": "google/paligemma-3b-pt-224",
        "llava": "llava-hf/llava-1.5-7b-hf",
    }