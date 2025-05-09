import streamlit as st
import os
import json
import re
from google import genai
from utils.database import get_doctors
from utils.user_history import add_history_entry


GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

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
            import io
            file_bytes = uploaded_file.read()
            file_name = uploaded_file.name
            file_ext = os.path.splitext(file_name)[1].lower()
            client = genai.Client(api_key=GEMINI_API_KEY)
            prompt = "Analyze this medical report and suggest the top 1-2 doctor specializations to consult, and explain why. Respond ONLY in this JSON format: {\"specializations\": [\"specialization1\", ...], \"explanation\": \"...\"}"
            if file_ext == '.pdf':
                file_io = io.BytesIO(file_bytes)
                sample_doc = client.files.upload(
                    file=file_io,
                    config=dict(mime_type='application/pdf')
                )
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[sample_doc, prompt]
                )
            else:
                file_io = io.BytesIO(file_bytes)
                sample_doc = client.files.upload(
                    file=file_io,
                    config=dict(mime_type='image/jpeg' if file_ext in ['.jpeg', '.jpg'] else 'image/png')
                )
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[sample_doc, prompt]
                )
            ai_text = response.text
            result_json = extract_json(ai_text)
            if result_json and 'specializations' in result_json:
                specialization = ', '.join(result_json['specializations'])
                user_id = st.session_state.user.get("id")
                st.success(f"Recommended Specialist: {specialization}")
                st.markdown(f"**AI Explanation:** {result_json.get('explanation', '')}")
                # Ask Gemini for further tests and costs
                test_prompt = f"Given the medical report and the suggested specialization ({specialization}), recommend further diagnostic tests to pinpoint the disease, along with their approximate costs in INR (Rs). Present as a list."
                # Call Gemini API again for test recommendations
                test_response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[sample_doc, test_prompt]
                )
                tests_text = test_response.text
                st.info("**Recommended Further Tests & Costs:**\n" + tests_text)
                # Save to user history
                add_history_entry(user_id, "report_analysis", {
                    "file_name": file_name,
                    "specialization": specialization,
                    "tests": tests_text
                })
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
