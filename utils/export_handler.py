import json
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def export_to_txt(ocr_text, art_analysis, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""HANDWRITTEN ART NOTES ANALYZER - EXPORT
Generated: {timestamp}

{'='*60}
EXTRACTED HANDWRITING
{'='*60}

{ocr_text}

{'='*60}
ARTWORK ANALYSIS
{'='*60}

{art_analysis}

{'='*60}
End of Report
"""
    return content

def export_to_json(ocr_text, art_analysis, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    data = {
        "timestamp": timestamp,
        "version": "1.0",
        "results": {
            "handwriting": ocr_text,
            "art_analysis": art_analysis
        }
    }
    
    return json.dumps(data, indent=2)

def export_to_pdf(ocr_text, art_analysis, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
    )
    
    story.append(Paragraph("Handwritten Art Notes Analyzer", title_style))
    story.append(Paragraph(f"Generated: {timestamp}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Extracted Handwriting", heading_style))
    story.append(Paragraph(ocr_text.replace('\n', '<br/>'), styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Artwork Analysis", heading_style))
    story.append(Paragraph(art_analysis.replace('\n', '<br/>'), styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def get_filename(format_type):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"analysis_{timestamp}.{format_type}"