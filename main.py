from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
import io

from ml_pipeline.preprocess import preprocess_eeg
from ml_pipeline.features import extract_features, extract_bands
from ml_pipeline.model import predict_risk
from ml_pipeline.explainability import generate_shap_values, generate_brain_heatmap, generate_waveform_image
from ml_pipeline.report import generate_clinical_report
from ml_pipeline.speech import analyze_audio_bytes
import base64

app = FastAPI(title="EEG-Based Schizophrenia Detection API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

import traceback

@app.post("/api/upload")
async def upload_eeg(file: UploadFile = File(...), patient_name: str = Form("Diagnostic Patient")):
    """
    Receives an .edf file and runs the full pipeline.
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Preprocess
        raw = preprocess_eeg(file_path)
        
        # Extract Features
        feature_vector = extract_features(raw)
        bands = extract_bands(raw)
        
        # Predict
        prediction = predict_risk(feature_vector)
        
        # Explainability
        shap_values = generate_shap_values(feature_vector)
        brain_map = generate_brain_heatmap(feature_vector)
        waveform_bytes = generate_waveform_image(raw)
        
        # AI Explanation
        try:
            from g4f.client import Client
            client = Client()
            prompt = f"Write a 3 sentence professional clinical explanation for patient '{patient_name}' with Schizophrenia AI risk score {prediction['risk_score']}/100 and band powers: {bands}. Conclude with 'Please consult a psychiatric professional.'"
            response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], web_search=False)
            ai_explanation = str(response.choices[0].message.content)
        except Exception:
            ai_explanation = f"Based on the analysis, {patient_name} exhibits a {prediction['category'].lower()} profile for schizophrenia indicators. The model detected an overall risk score of {prediction['risk_score']}/100 driven by the extracted EEG band powers. Please consult a psychiatric professional for a complete clinical evaluation."
            
        # Report
        pdf_bytes = generate_clinical_report(prediction, bands, patient_name, ai_explanation, waveform_bytes)
        pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        return {
            "status": "success",
            "results": {
                "prediction": prediction,
                "bands": bands,
                "explainability": {
                    "shap": shap_values,
                    "brain_map": brain_map
                },
                "report_b64": pdf_b64
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}

@app.post("/analyze-speech")
async def analyze_speech(audio: UploadFile = File(...)):
    """
    Receives raw microphone byte stream from Streamlit UI, extracts audio, 
    generates transcript, and runs psychiatric NLP analysis via g4f metrics.
    """
    try:
        audio_bytes = await audio.read()
        analysis = analyze_audio_bytes(audio_bytes)
        return {
            "status": "success",
            "data": analysis
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "traceback": traceback.format_exc()}
