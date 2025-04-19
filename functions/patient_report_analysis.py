import streamlit as st
import os
import google.generativeai as genai
import json
import re
from utils.database import get_doctors

GEMINI_API_KEY = "AIzaSyBNeVIUC4v1I8dptR4w6YvAVhhqvA1KZAw"

def extract_json(text):
    text = text.strip()
    if text.startswith('```'):
        text = re.sub(r'^```[a-zA-Z]*', '', text)
        text = text.strip('`\n')
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except Exception:
            pass
    return None

def show():
    st.title("Medical Report Analysis (AI)")
    st.info("Upload your medical report (PDF, PNG, JPEG). Gemini AI will analyze and suggest a specialist.")

    uploaded_file = st.file_uploader(
        "Upload Report (PDF, PNG, JPEG)",
        type=["pdf", "png", "jpeg", "jpg"],
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        if not GEMINI_API_KEY:
            st.error("Gemini API key not set. Please contact admin.")
            return
        try:
            file_bytes = uploaded_file.read()
            file_name = uploaded_file.name
            file_ext = os.path.splitext(file_name)[1].lower()
            # Use file_bytes directly for PDF inference
            if file_ext == '.pdf':
                gemini_input = {"file": file_bytes, "file_type": "pdf"}
            else:
                gemini_input = {"file": file_bytes, "file_type": "image"}
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-pro-vision")
            response = model.generate_content([
                "Analyze this medical report and suggest the top 1-2 doctor specializations to consult, and explain why. Respond ONLY in this JSON format: {\"specializations\": [\"specialization1\", ...], \"explanation\": \"...\"}",
                gemini_input
            ])
            ai_text = response.text
            result_json = extract_json(ai_text)
            if result_json and 'specializations' in result_json:
                st.success(f"Recommended Specializations: {', '.join(result_json['specializations'])}")
                st.markdown(f"**AI Explanation:** {result_json.get('explanation', '')}")
                doctors = get_doctors()
                matched = [doc for doc in doctors if any(
                    spec.lower() in doc.get('specialization', '').lower() for spec in result_json['specializations'])]
                if matched:
                    st.subheader("Matching Doctors:")
                    for doc in matched:
                        st.write(f"Dr. {doc['username']} ({doc.get('specialization', 'General')})")
                        if st.button("Book Appointment", key=f"book_{doc['id']}"):
                            st.session_state.selected_doctor_id = doc['id']
                            st.session_state.current_page = 'appointment'
                            st.rerun()
                else:
                    st.info("No doctors found with the recommended specialization.")
            else:
                st.info("No specialization could be extracted from Gemini's response.")
        except Exception as e:
            st.error(f"Error communicating with Gemini: {e}. Raw response: {locals().get('ai_text', 'No response')}")
