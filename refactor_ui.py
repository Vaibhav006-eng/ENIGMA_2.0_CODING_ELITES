import os

with open("streamlit_app/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find insertion point
insert_idx = -1
for i, line in enumerate(lines):
    if "uploaded_file = st.file_uploader" in line:
        insert_idx = i
        break

if insert_idx != -1:
    new_lines = lines[:insert_idx]
    
    # Add AI Assistant Tab
    tab_code = """
tab_dashboard, tab_assistant = st.tabs(["🔬 Diagnostic Dashboard", "🤖 Medical AI Assistant"])

with tab_assistant:
    st.markdown("<div class='glass-panel'><h3>NeuroSync Clinical Assistant</h3><p>Powered by Gemini AI. Ask questions about EEG patterns, Schizophrenia markers, or clinical literature.</p></div>", unsafe_allow_html=True)
    
    api_key = st.text_input("Enter your Google Gemini API Key:", type="password", help="Your key is not stored and is only used for this session.")
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="You are NeuroSync AI, a highly advanced medical AI assistant embedded within an EEG Schizophrenia analysis platform. You communicate like a professional clinical assistant. Answer questions directly, accurately, and concisely. Focus on neuroscience, EEG artifacts, frequency bands, brain mapping, and Schizophrenia markers. Format your outputs neatly.")
            
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
                
            for role, text in st.session_state.chat_history:
                with st.chat_message(role):
                    st.markdown(text)
                    
            if prompt := st.chat_input("Ask a clinical or technical question..."):
                st.session_state.chat_history.append(("user", prompt))
                with st.chat_message("user"):
                    st.markdown(prompt)
                    
                with st.chat_message("assistant"):
                    try:
                        chat = model.start_chat(history=[{"role": "user" if r=="user" else "model", "parts": [t]} for r,t in st.session_state.chat_history[:-1]])
                        response = chat.send_message(prompt)
                        st.markdown(response.text)
                        st.session_state.chat_history.append(("assistant", response.text))
                    except Exception as e:
                        st.error(f"Error communicating with AI: {e}")
        except Exception as e:
            st.error(f"API Key Error: {e}")
    else:
        st.info("Please provide your Gemini API key above to activate the assistant.")

with tab_dashboard:
"""
    new_lines.append(tab_code)
    
    # Indent the rest of the lines
    for line in lines[insert_idx:]:
        new_lines.append("    " + line)
        
    # Add import at the top
    for i, line in enumerate(new_lines):
        if "import streamlit as st" in line:
            new_lines.insert(i+1, "import google.generativeai as genai\n")
            break

    with open("streamlit_app/app.py", "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("Refactoring complete.")
else:
    print("Insertion point not found.")
