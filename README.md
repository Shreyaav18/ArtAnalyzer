# Handwritten Art Notes Analyzer

An AI-powered application that extracts handwritten text and analyzes artwork from images using vision-language models.

## Features

- **Handwriting OCR**: Extract and digitize handwritten text from images
- **Art Analysis**: Identify art styles, techniques, medium, and historical context
- **Export Options**: Download results in TXT, JSON, or PDF format
- **Session History**: Track and reload previous analyses
- **Dual Processing**: Handle images with both text and artwork simultaneously

## Tech Stack

- **AI Model**: Salesforce BLIP-2 (vision-language model)
- **Framework**: Gradio, Transformers, PyTorch
- **Processing**: PIL/Pillow, ReportLab
- **Deployment**: Hugging Face Spaces

## Installation

```bash
git clone https://github.com/Shreyaav18/handwritten-art-analyzer.git
cd handwritten-art-analyzer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory:

```
HF_TOKEN=your_huggingface_token_here
```

Get your token from [Hugging Face Settings](https://huggingface.co/settings/tokens)

## Usage

```bash
python app.py
```

The application will launch in your browser at `http://localhost:7860`

### Workflow

1. Upload an image containing handwritten notes and/or artwork
2. Click "Analyze" to process the image
3. View extracted text and art analysis in separate panels
4. Export results in your preferred format
5. Access previous analyses through session history

## Project Structure

```
handwritten-art-analyzer/
├── app.py                  # Main application
├── requirements.txt        # Dependencies
├── .env                    # Configuration
└── utils/
    ├── model_loader.py     # Model initialization
    ├── ocr_handler.py      # Handwriting extraction
    ├── art_analyzer.py     # Artwork analysis
    ├── export_handler.py   # Export functionality
    └── history_manager.py  # Session management
```

## Model Information

Currently using `Salesforce/blip2-opt-2.7b` for image-text-to-text tasks. Alternative models can be configured in `utils/model_loader.py`.

## Requirements

- Python 3.8+
- CUDA-compatible GPU (recommended) or CPU
- 8GB+ RAM
- Hugging Face account

## Future Enhancements

- RAG integration for deeper art history knowledge
- Multi-language support
- Batch processing capabilities
- Advanced image preprocessing

## Acknowledgments

- Salesforce for BLIP-2 model
- Hugging Face for infrastructure
- Gradio for UI framework