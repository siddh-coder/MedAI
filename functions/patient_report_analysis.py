import streamlit as st
import tempfile
import os
from google import genai

GEMINI_API_KEY = "AIzaSyBNeVIUC4v1I8dptR4w6YvAVhhqvA1KZAw"
def show():
    st.title("Medical Report Analysis (AI)")
    st.info("Upload your medical report (PDF, PNG, JPEG). Gemini AI will analyze and suggest a specialist.")

    uploaded_file = st.file_uploader(
        "Upload Report (PDF, PNG, JPEG)",
        type=["pdf", "png", "jpeg", "jpg"],
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        if not GEMINI_API_KEY:
            st.error("Gemini API key not set. Please provide your API key in the script.")
            os.unlink(tmp_path)
            return

        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            myfile = client.files.upload(file=tmp_path)
            # Custom prompt to get structured specializations
            prompt = (
                "Analyze this medical report and recommend which type(s) of doctor the patient should be referred to. "
                "Please output your answer as a JSON object with a 'specializations' field, which is a list of recommended specializations. "
                "Example: {\"specializations\": [\"cardiologist\", \"endocrinologist\"]}. "
                "If you have a textual explanation, include it in an 'explanation' field."
            )
            with st.spinner("Analyzing with Gemini..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[myfile, prompt]
                )
            import json
            import re
            st.subheader("Gemini AI Recommendation")
            def extract_json(text):
                # Remove markdown code block markers
                text = text.strip()
                if text.startswith('```'):
                    text = re.sub(r'^```[a-zA-Z]*', '', text)
                    text = text.strip('`\n')
                # Extract first JSON object
                match = re.search(r'\{[\s\S]*\}', text)
                if match:
                    json_str = match.group(0)
                    try:
                        return json.loads(json_str)
                    except Exception:
                        pass
                return None
            gemini_data = extract_json(response.text)
            if gemini_data:
                specializations = gemini_data.get("specializations", [])
                explanation = gemini_data.get("explanation", "")
            else:
                specializations = []
                explanation = response.text
            st.write(explanation)
            if specializations:
                st.markdown("### Doctors Matching Recommendation:")
                from utils.database import get_doctors
                doctors = get_doctors()
                matched = [d for d in doctors if str(d.get('specialization', '')).strip().lower() in [s.lower() for s in specializations]]
                if matched:
                    for doc in matched:
                        col1, col2 = st.columns([3,1])
                        with col1:
                            st.write(f"**Dr. {doc['username']}**  ")
                            st.write(f"Specialization: {doc.get('specialization','N/A')}")
                            st.write(f"Experience: {doc.get('experience','N/A')} years")
                        with col2:
                            if st.button(f"Book Appointment", key=f"book_{doc['id']}"):
                                st.session_state.selected_doctor_id = doc['id']
                                st.session_state.current_page = 'appointment'
                                st.rerun()
                else:
                    st.info("No doctors found with the recommended specialization.")
            else:
                st.info("No specialization could be extracted from Gemini's response.")
        except Exception as e:
            st.error(f"Error communicating with Gemini: {e}")
        finally:
            os.unlink(tmp_path)
