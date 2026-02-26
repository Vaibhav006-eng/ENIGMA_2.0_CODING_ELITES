import streamlit as st
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from streamlit_mic_recorder import mic_recorder
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

try:
    LOGO_B64 = get_base64_image("streamlit_app/assets/logo.png")
    BANNER_B64 = get_base64_image("streamlit_app/assets/banner.png")
    BRAIN_B64 = get_base64_image("streamlit_app/assets/brain_icon.png")
except:
    LOGO_B64 = ""
    BANNER_B64 = ""
    BRAIN_B64 = ""

# Page Config
st.set_page_config(page_title="NeuroSync | SZ Detection", layout="wide", page_icon="🧠")

# Inject Custom CSS
with open('streamlit_app/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# API Endpoint
API_URL = "http://localhost:8000/api/upload"

def mock_topomap_3d(intensity_factor):
    """Generates a 3D brain scatter plot for visualization."""
    u = np.random.uniform(0, 2 * np.pi, 500)
    v = np.random.uniform(0, np.pi / 2, 500) # Hemisphere
    
    x = np.sin(v) * np.cos(u) + np.random.normal(0, 0.05, 500)
    y = np.sin(v) * np.sin(u) + np.random.normal(0, 0.05, 500)
    z = np.cos(v) + np.random.normal(0, 0.05, 500)
    
    # Simulate anomalous frontal activity based on intensity
    values = np.where(y > 0.4, np.random.normal(intensity_factor * 10, 0.2, 500), np.random.normal(2, 0.1, 500))
    
    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=4,
            color=values,
            colorscale='electric',
            opacity=0.8,
            showscale=False
        )
    )])
    
    fig.update_layout(
        title={'text': "3D Neural Activity Overlay", 'font': {'color': '#00f0ff', 'family': 'Inter'}},
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, visible=False),
            yaxis=dict(showbackground=False, showticklabels=False, visible=False),
            zaxis=dict(showbackground=False, showticklabels=False, visible=False),
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320
    )
    return fig

def render_gauge(risk_score, category):
    color = "#00f0ff" if risk_score < 30 else "#f59e0b" if risk_score < 60 else "#ff003c"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score,
        title = {'text': f"CLINICAL RISK: {category.upper()}", 'font': {'color': '#94a3b8', 'size': 16, 'family': 'Inter'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "rgba(0,255,255,0.2)"},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': "rgba(10,25,47,0.5)",
            'borderwidth': 1,
            'bordercolor': "rgba(0,255,255,0.1)",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(0, 240, 255, 0.1)'},
                {'range': [30, 60], 'color': 'rgba(245, 158, 11, 0.1)'},
                {'range': [60, 100], 'color': 'rgba(255, 0, 60, 0.1)'}],
        },
        number={'font': {'color': '#00f0ff'}}
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"), margin=dict(l=20,r=20,t=50,b=20), height=300)
    return fig


if LOGO_B64 and BANNER_B64:
    header_html = f"""
    <div class='main-header' style='background-image: linear-gradient(rgba(10, 25, 47, 0.85), rgba(0, 31, 63, 0.95)), url("data:image/png;base64,{BANNER_B64}"); background-size: cover; background-position: center; border: 1px solid rgba(0, 255, 255, 0.3); box-shadow: 0 0 40px rgba(0, 240, 255, 0.2);'>
        <img src="data:image/png;base64,{LOGO_B64}" style="width: 120px; border-radius: 20%; box-shadow: 0 0 20px rgba(0,255,255,0.5); margin-bottom: 15px;">
        <h1 style="text-shadow: 0 0 20px rgba(0, 240, 255, 0.8);">NEUROSYNC AI ENGINE</h1>
        <p style="color: #cbd5e1; font-weight: 400; font-size: 1.2rem; letter-spacing: 1px;">Advanced EEG Schizophrenia Risk Detection & Neural Mapping</p>
    </div>
    """
else:
    header_html = "<div class='main-header'><h1>🧠 Clinical AI Node</h1><p>NeuroSync // Automated EEG Analysis Hub</p></div>"

st.markdown(header_html, unsafe_allow_html=True)


tab_dashboard, tab_assistant, tab_test, tab_voice = st.tabs(["🔬 Diagnostic Dashboard", "🤖 Medical AI Assistant", "📝 Psychological Screening", "🎙️ Voice Biomarker Analysis"])

with tab_voice:
    st.markdown(f"""
    <div class='glass-panel' style='text-align: center'>
        <img src="data:image/png;base64,{BRAIN_B64}" width="80px" class="animated-brain">
        <h3>Linguistic Symptom Tracking</h3>
        <p>Record your voice to scan for schizophrenia speech markers such as derailment, tangentiality, and poverty of speech.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Click to start recording microphone (try 15-30s)**")
        audio = mic_recorder(
            start_prompt="🔴 Start Recording",
            stop_prompt="⏹️ Stop Recording",
            just_once=False,
            use_container_width=True,
            format="webm",
            key='mic_recorder'
        )
        
    with col2:
        if audio:
            st.audio(audio['bytes'])
            if st.button("🚀 Analyze Vocal Biomarkers", use_container_width=True, type="primary"):
                with st.spinner("Transcribing audio & running g4f NLP psychiatric analysis..."):
                    files = {"audio": ("recording.webm", audio['bytes'], "audio/webm")}
                    try:
                        voice_url = API_URL.replace("/api/upload", "/analyze-speech")
                        res = requests.post(voice_url, files=files)
                        if res.status_code == 200:
                            data = res.json()
                            if data.get("status") == "success":
                                analysis = data["data"]
                                st.success("Analysis Complete")
                                
                                # UI Cards
                                color = "#00f0ff"
                                if analysis['disorder_risk'] == 'High': color = "#ff003c"
                                elif analysis['disorder_risk'] == 'Moderate': color = "#f59e0b"
                                
                                st.markdown(f"""
<div class='glass-panel' style='border-left: 5px solid {color};'>
    <h4 style='color: white; margin-bottom: 5px;'>Recognized Transcript</h4>
    <p style='color: #cbd5e1; font-style: italic;'>"{analysis['transcript']}"</p>
    
    <div style='display: flex; justify-content: space-between; margin-top: 15px;'>
        <div><span style='color: #94a3b8;'>Detected Risk Level:</span> <strong style='color: {color}; font-size: 1.2rem;'>{analysis['disorder_risk']}</strong></div>
        <div><span style='color: #94a3b8;'>NLP Confidence:</span> <strong style='color: white;'>{int(analysis['confidence']*100)}%</strong></div>
    </div>
    
    <hr style='border-color: rgba(255,255,255,0.1); margin: 15px 0;'>
    <h4 style='color: white; margin-bottom: 5px;'>AI Clinical Assessment</h4>
    <p style='color: #00f0ff;'>{analysis['analysis']}</p>
</div>
""", unsafe_allow_html=True)
                            else:
                                st.error(f"Analysis failed: {data.get('message', 'Unknown error')}")
                        else:
                            st.error(f"Connection failed: {res.status_code}")
                    except Exception as e:
                        st.error(f"Request failed: {e}")

with tab_assistant:
    st.markdown(f"""
    <div class='glass-panel' style='text-align: center'>
        <img src="data:image/png;base64,{BRAIN_B64}" width="100px" class="animated-brain" style="filter: hue-rotate(45deg);">
        <h3>NeuroSync Clinical Assistant</h3>
        <p>Powered by NeuroSync AI Engine. Ask questions about EEG patterns, Schizophrenia markers, or clinical literature without needing an API key.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are NeuroSync AI, a highly advanced medical AI assistant embedded within an EEG Schizophrenia analysis platform. You communicate like a professional clinical assistant. Answer questions directly, accurately, and concisely. Focus on neuroscience, EEG artifacts, frequency bands, brain mapping, and Schizophrenia markers. Format your outputs neatly."}
        ]
        
    for msg in st.session_state.chat_history:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    if prompt := st.chat_input("Ask a clinical or technical question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Analyzing medical context..."):
                try:
                    from g4f.client import Client
                    client = Client()
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=st.session_state.chat_history,
                        web_search=False
                    )
                    answer = response.choices[0].message.content
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error communicating with AI: {e}")

with tab_test:
    st.markdown("<div class='glass-panel'><h3>Clinical Symptom Questionnaire</h3><p>Self-reported 15-point screening for early signs of psychosis and schizophrenia.</p></div>", unsafe_allow_html=True)
    
    questions = [
        "Do you hear voices when no one is around?",
        "Do you feel like someone is watching or spying on you without proof?",
        "Do you believe people are plotting against you?",
        "Do you see things that others cannot see?",
        "Do your thoughts sometimes feel controlled by someone else?",
        "Do you feel like your thoughts are being broadcast so others can hear them?",
        "Do you have difficulty organizing your thoughts while speaking?",
        "Do people often say your speech is confusing or hard to understand?",
        "Do you feel emotionally numb or unable to express feelings?",
        "Have you lost interest in activities you once enjoyed?",
        "Do you isolate yourself from friends or family without clear reason?",
        "Do you struggle to concentrate on simple tasks?",
        "Do you feel suspicious of close family members?",
        "Do you believe you have special powers or abilities others don’t?",
        "Have these experiences lasted for more than one month?"
    ]
    
    score = 0
    with st.form("schizophrenia_screening_form"):
        st.write("Please answer the following questions as honestly as possible based on your recent experiences.")
        
        responses = []
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}: {q}**")
            resp = st.radio(f"Select an answer for Q{i+1}", ["No", "Yes"], key=f"q_{i}", index=0, horizontal=True, label_visibility="collapsed")
            responses.append(resp)
            st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px; border-color: rgba(0,255,255,0.1);'>", unsafe_allow_html=True)
            
        submitted = st.form_submit_button("Submit Assessment", type="primary")
        
        if submitted:
            score = sum([1 for r in responses if r == "Yes"])
            max_score = len(questions)
            
            risk_cat = "Low"
            color = "#00f0ff"
            if score >= 10:
                risk_cat = "High"
                color = "#ff003c"
            elif score >= 5:
                risk_cat = "Moderate"
                color = "#f59e0b"
                
            st.markdown(f"""
            <div class='glass-panel' style='border-color: {color}; text-align: center; margin-top: 20px;'>
                <h2 style='color: {color}; margin-bottom: 0px;'>Analysis Complete</h2>
                <h1 style='color: {color}; font-size: 3rem; margin: 10px 0px;'>{score}/{max_score}</h1>
                <p style='color: white; font-size: 1.2rem;'>Psychological Risk Level: <b>{risk_cat}</b></p>
                <p style='color: #94a3b8; font-size: 0.9rem;'>Disclaimer: This screening tool does not replace professional clinical diagnosis. If you are experiencing distress, please contact a healthcare professional.</p>
            </div>
            """, unsafe_allow_html=True)

with tab_dashboard:
    patient_name = st.text_input("📝 Patient ID / Name", value="Patient_001", help="Enter the patient's identifier to be stamped onto the final PDF clinical report.")
    uploaded_file = st.file_uploader("Upload EEG Recording (.edf, .fif)", type=['edf', 'fif'])
    
    if uploaded_file is not None:
        st.markdown("<div class='glass-panel'>Analyzing signals...</div>", unsafe_allow_html=True)
        with st.spinner("Processing EEG data, running artifact removal, and extracting features..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/octet-stream")}
            post_data = {"patient_name": patient_name}
            try:
                res = requests.post(API_URL, files=files, data=post_data)
                if res.status_code == 200:
                    data = res.json()
                    if data["status"] == "success":
                        st.success("Analysis Complete")
                        
                        results = data["results"]
                        pred = results["prediction"]
                        bands = results["bands"]
                        explain = results["explainability"]
                        
                        col1, col2 = st.columns(2)
                        
                        # Col 1: Risk & Bands
                        with col1:
                            st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                            st.plotly_chart(render_gauge(pred['risk_score'], pred['category']), use_container_width=True)
                            st.markdown(f"**Confidence Interval:** {pred['confidence']*100}%")
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            st.markdown("<div class='glass-panel'><h3>Frequency Band Power</h3>", unsafe_allow_html=True)
                            # Frequency bands bar chart
                            band_keys = list(bands.keys())
                            band_vals = list(bands.values())
                            fig_bands = go.Figure(data=[go.Bar(
                                x=band_keys, 
                                y=band_vals, 
                                marker_color=['rgba(0,240,255,0.8)', 'rgba(59,130,246,0.8)', 'rgba(99,102,241,0.8)', 'rgba(139,92,246,0.8)', 'rgba(236,72,153,0.8)'],
                                marker_line_width=1,
                                marker_line_color='rgba(255,255,255,0.2)'
                            )])
                            fig_bands.update_layout(
                                paper_bgcolor="rgba(0,0,0,0)", 
                                plot_bgcolor="rgba(0,0,0,0)", 
                                font=dict(color="#94a3b8"),
                                margin=dict(l=0, r=0, t=10, b=0),
                                height=300
                            )
                            st.plotly_chart(fig_bands, use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                        # Col 2: Brain Map & SHAP
                        with col2:
                            st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                            st.plotly_chart(mock_topomap_3d(pred['probability']), use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            st.markdown("<div class='glass-panel'><h3>Feature Importance (SHAP)</h3>", unsafe_allow_html=True)
                            shap_features = [s['feature'] for s in explain['shap']]
                            shap_vals = [s['importance'] for s in explain['shap']]
                            fig_shap = go.Figure(data=[go.Bar(
                                x=shap_vals, 
                                y=shap_features, 
                                orientation='h', 
                                marker_color='rgba(0, 240, 255, 0.7)',
                                marker_line_color='#00f0ff',
                                marker_line_width=1
                            )])
                            fig_shap.update_layout(
                                yaxis={'categoryorder':'total ascending'}, 
                                paper_bgcolor="rgba(0,0,0,0)", 
                                plot_bgcolor="rgba(0,0,0,0)", 
                                font=dict(color="#94a3b8"),
                                margin=dict(l=0, r=0, t=10, b=0),
                                height=300
                            )
                            st.plotly_chart(fig_shap, use_container_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                        # Download Report
                        import base64
                        pdf_bytes = base64.b64decode(results['report_b64'])
                        st.download_button(
                            label="🖺 Download AI-Enhanced Clinical PDF",
                            data=pdf_bytes,
                            file_name=f"neurosync_report_{patient_name.replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    else:
                        st.error(f"Error from API: {data.get('message', 'Unknown error')}")
            except Exception as e:
                st.error(f"Could not connect to backend server: {e}")
