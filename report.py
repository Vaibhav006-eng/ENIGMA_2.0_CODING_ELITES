from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import datetime

def generate_clinical_report(prediction_data, bands_data, patient_name, ai_explanation, waveform_bytes):
    """
    Generates a PDF Clinical Report in memory and returns bytes.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Header styling
    c.setFillColorRGB(0.04, 0.07, 0.16) # Navy background header
    c.rect(0, height - 80, width, 80, fill=1, stroke=0)
    
    c.setFillColorRGB(0, 0.94, 1.0) # Cyan text
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "NeuroSync AI Clinical Report")
    
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 120, "Patient Details")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 140, f"Name: {patient_name}")
    c.drawString(50, height - 160, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Analysis Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 200, "Diagnostic Prediction:")
    
    color = (0.06, 0.72, 0.5) if prediction_data['risk_score'] < 30 else (0.96, 0.62, 0.04) if prediction_data['risk_score'] < 60 else (1.0, 0.0, 0.23)
    c.setFillColorRGB(*color)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, height - 200, f"{prediction_data['category'].upper()}")
    
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 225, f"AI Risk Score: {prediction_data['risk_score']}/100")
    c.drawString(50, height - 245, f"Model Confidence: {int(prediction_data['confidence']*100)}%")
    
    # Frequency Bands
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 285, "Frequency Band Powers (µV²):")
    c.setFont("Helvetica", 12)
    y = height - 310
    for band, power in bands_data.items():
        c.drawString(60, y, f"- {band}: {power}")
        y -= 20
        
    # Waveform Image
    if waveform_bytes:
        try:
            img_io = io.BytesIO(waveform_bytes)
            img = ImageReader(img_io)
            c.drawImage(img, 50, y - 180, width=450, height=150, preserveAspectRatio=True)
            y -= 200
        except Exception as e:
            c.drawString(50, y - 20, f"[Waveform unrenderable: {e}]")
            y -= 40
            
    # AI Explanation
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 30, "AI Generated Explanation:")
    c.setFont("Helvetica", 10)
    
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph
    styles = getSampleStyleSheet()
    p = Paragraph(ai_explanation, styles['Normal'])
    p.wrapOn(c, width - 100, 200)
    p.drawOn(c, 50, y - 30 - p.height - 10)
        
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(50, 40, "Disclaimer: This AI analysis is an assistive tool and does not replace psychiatric evaluation.")
    
    c.save()
    buffer.seek(0)
    return buffer.read()
