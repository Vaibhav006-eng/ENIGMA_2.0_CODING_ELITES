import speech_recognition as sr
import io
import os
import requests
import json
import subprocess
import imageio_ffmpeg
import requests
import json

def analyze_audio_bytes(audio_bytes):
    """
    Converts webm/wav bytes to wav format if needed, extracts transcript using local SpeechRecognition,
    then uses g4f (GPT-4) to analyze the transcript for Schizophrenia speech markers.
    """
    try:
        # Convert webm to wav using imageio_ffmpeg binary
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        
        # Write bytes to temp file because ffmpeg needs a file path
        temp_in = "temp_audio.webm"
        temp_out = "temp_audio.wav"
        
        with open(temp_in, "wb") as f:
            f.write(audio_bytes)
            
        # Run conversion
        subprocess.run([ffmpeg_exe, "-y", "-i", temp_in, temp_out], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        with open(temp_out, "rb") as f:
            wav_data = f.read()
            
        # Cleanup
        if os.path.exists(temp_in): os.remove(temp_in)
        if os.path.exists(temp_out): os.remove(temp_out)
            
        wav_io = io.BytesIO(wav_data)
        
        # Recognize Speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            try:
                transcript = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                transcript = "[Could not understand audio]"
            except sr.RequestError as e:
                transcript = f"[Speech recognition service unavailable: {e}]"
        
        # If no transcript, return default
        if not transcript or transcript.startswith("[Could not"):
            return {
                "transcript": transcript,
                "confidence": 0.0,
                "disorder_risk": "Undetermined",
                "analysis": "No coherent speech detected for analysis."
            }
            
        # Analyze Transcript for Vocal Biomarkers using LLM
        try:
            from g4f.client import Client
            client = Client()
            prompt = (
                f"Act as a psychiatric AI. Analyze the following transcript for linguistic markers of schizophrenia "
                f"(e.g., tangentiality, derailment, poverty of speech, illogicality). Provide a short 3-sentence analysis.\n"
                f"Transcript: '{transcript}'\n\n"
                f"Also, provide a risk level (Low, Moderate, High) and a confidence percentage (e.g., 85) in JSON format "
                f"like this: {{\"risk\": \"Moderate\", \"confidence\": 85, \"analysis\": \"your 3 sentences\"}}"
            )
            response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}], web_search=False)
            
            # Parse JSON block from response
            res_text = response.choices[0].message.content
            # Extract JSON if wrapped in markdown
            if "```json" in res_text:
                res_text = res_text.split("```json")[1].split("```")[0]
            elif "```" in res_text:
                res_text = res_text.split("```")[1].split("```")[0]
                
            res_json = json.loads(res_text.strip())
            
            return {
                "transcript": transcript,
                "confidence": res_json.get("confidence", 50) / 100.0,
                "disorder_risk": res_json.get("risk", "Undetermined"),
                "analysis": res_json.get("analysis", "Analysis completed.")
            }
            
        except Exception as e:
            return {
                "transcript": transcript,
                "confidence": 0.5,
                "disorder_risk": "Unknown",
                "analysis": f"AI Parsing error: {str(e)}"
            }
            
    except Exception as e:
        raise Exception(f"Audio processing failure: {str(e)}")
