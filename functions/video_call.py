import streamlit as st
import streamlit.components.v1 as components
import tempfile
import os
from utils.user_history import add_history_entry
from utils.database import get_patient_appointments, get_doctor_appointments, save_prescription
from datetime import datetime, timedelta
import requests
import whisper

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def generate_meeting_url(appointment_id):
    base_url = "https://meet.jit.si/"
    room_name = f"MedAI_{appointment_id}"
    return base_url + room_name

def speech_to_text(audio_bytes):
    # Use Whisper (openai-whisper) locally for free speech-to-text
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_audio:
        tmp_audio.write(audio_bytes)
        tmp_audio_path = tmp_audio.name
    model = whisper.load_model("base")  # or "tiny" for faster, less accurate
    result = model.transcribe(tmp_audio_path)
    os.remove(tmp_audio_path)
    return result["text"].strip()

def generate_prescription(transcript):
    # Use Gemini or Hugging Face LLM to generate prescription
    if not GEMINI_API_KEY:
        return "Gemini API key not set."
    from google import genai
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = (
        "Given the following transcript of a doctor's instructions, generate a structured medical prescription including: "+
        "1) Medicines (name, dosage, frequency), 2) Diagnosis, 3) Next steps/recommendations. Format as a clear prescription.\nTranscript: " + transcript
    )
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[prompt]
    )
    return response.text.strip()

def ai_summarize_meeting(messages):
    if not GEMINI_API_KEY:
        return "Gemini API key not set."
    client = genai.Client(api_key=GEMINI_API_KEY)
    chat_text = '\n'.join([f"{m['role']}: {m['content']}" for m in messages])
    prompt = (
        "Given the following doctor-patient chat and AI-detected symptoms, summarize the meeting. "
        "Extract and list: 1) Medicines suggested by the doctor, 2) Diagnosis, 3) Next steps or recommendations. "
        "Format output as a clear summary for medical records."
    )
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[f"{prompt}\n\n{chat_text}"]
    )
    return response.text.strip()

def show():
    st.title("Video Consultation")
    st.markdown("Connect with your doctor through a secure video call.")
    
    if not st.session_state.authenticated:
        st.error("Please log in to access video consultations.")
        return
    
    st.subheader("Start a Video Call")
    appointment_id = st.text_input("Enter Appointment ID")
    user = st.session_state.user
    user_id = user.get("id")
    user_type = st.session_state.get("user_type", "")
    
    appointment_ok = False
    appointment_data = None
    now = datetime.now()
    if appointment_id:
        appointments = []
        if user_type == 'patient':
            appointments = get_patient_appointments(user_id)
        elif user_type == 'doctor':
            appointments = get_doctor_appointments(user_id)
        for apt in appointments:
            if str(apt.get('id')) == str(appointment_id):
                appointment_ok = True
                break
        if not appointment_ok:
            st.error("You are not authorized to join this appointment, or it is not within the scheduled time window.")
            return
    
    if appointment_ok:
        meeting_url = generate_meeting_url(appointment_id)
        st.markdown(f"[Join Video Call in new tab]({meeting_url})", unsafe_allow_html=True)
        components.html(
            f"""
            <iframe src=\"{meeting_url}\" allow=\"camera; microphone; fullscreen; display-capture\"
                    style=\"height:600px; width:100%; border:0;\"></iframe>
            """,
            height=600,
        )

        st.subheader("Prescription Recorder (Doctor Only)")
        if user_type == 'doctor':
            audio_file = st.file_uploader("Record or upload your prescription audio (WAV/MP3)", type=["wav", "mp3"])
            if audio_file is not None:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/wav')
                if st.button("Transcribe & Generate Prescription", key=f"transcribe_{appointment_id}"):
                    with st.spinner("Transcribing audio..."):
                        transcript = speech_to_text(audio_bytes)
                        st.write("**Transcript:**", transcript)
                    with st.spinner("Generating prescription..."):
                        prescription = generate_prescription(transcript)
                        st.write("**Prescription:**")
                        st.code(prescription)
                        # Save prescription for both doctor and patient
                        save_prescription(appointment_id, user_id, prescription)
                        st.success("Prescription saved for both doctor and patient.")
        else:
            st.info("Only the doctor can record and save prescriptions.")

        st.subheader("Live Chat & AI Room")
        if f"chat_{appointment_id}" not in st.session_state:
            st.session_state[f"chat_{appointment_id}"] = []
        chat = st.session_state[f"chat_{appointment_id}"]

        # Chat input
        col1, col2 = st.columns([3, 1])
        with col2:
            send_clicked = st.button("Send", key=f"send_btn_{appointment_id}")
        # Handle clearing input on next run
        clear_flag = f"clear_input_{appointment_id}"
        input_key = f"chat_input_{appointment_id}"
        if st.session_state.get(clear_flag):
            st.session_state[input_key] = ""
            st.session_state[clear_flag] = False
        with col1:
            user_msg = st.text_input("Type a message", key=input_key)
        if send_clicked and user_msg.strip():
            new_chat = chat + [{"role": user_type, "content": user_msg.strip()}]
            st.session_state[f"chat_{appointment_id}"] = new_chat
            st.session_state[clear_flag] = True

        # Display chat
        st.markdown("---")
        st.markdown("### Chat History")
        for m in chat:
            if m["role"] == "ai":
                st.info(m["content"])
            elif m["role"] == "doctor":
                st.markdown(f"**Doctor:** {m['content']}")
            elif m["role"] == "patient":
                st.markdown(f"**Patient:** {m['content']}")
            else:
                st.markdown(f"**{m['role'].capitalize()}:** {m['content']}")

        # AI Meeting Notes
        st.markdown("---")
        st.subheader("AI Meeting Summary & Save to History")
        if st.button("Summarize & Save", key=f"summarize_btn_{appointment_id}"):
            with st.spinner("Summarizing meeting with Gemini..."):
                summary = ai_summarize_meeting(chat)
            # Doctor validates/edits summary
            if user_type == "doctor":
                edited_summary = st.text_area("Review/Edit Meeting Summary before saving:", summary, key=f"summary_edit_{appointment_id}")
                if st.button("Confirm & Save to History", key=f"save_history_{appointment_id}"):
                    # Save to both doctor and patient history
                    add_history_entry(user_id, "meeting_summary", {"summary": edited_summary, "appointment_id": appointment_id})
                    # Try to get patient_id from chat or context if available
                    # Here, you would need to add logic to find the patient_id for this appointment
                    st.success("Summary saved to doctor's history. Please ensure it is also saved to the patient's history as needed.")
            else:
                st.info("Only the doctor can validate and save the meeting summary.")

    st.subheader("Tips for a Successful Call")
    st.markdown("""
    - Ensure a stable internet connection.
    - Use headphones for better audio quality.
    - Find a quiet, well-lit space for your consultation.
    """)
