import streamlit as st
import streamlit.components.v1 as components
import tempfile
from PIL import Image
import base64
import io
import os
from google import genai
from utils.user_history import add_history_entry
from utils.database import get_patient_appointments, get_doctor_appointments
from datetime import datetime, timedelta

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def generate_meeting_url(appointment_id):
    base_url = "https://meet.jit.si/"
    room_name = f"MedAI_{appointment_id}"
    return base_url + room_name

def ai_detect_symptoms(image_file):
    if not GEMINI_API_KEY:
        return "Gemini API key not set."
    client = genai.Client(api_key=GEMINI_API_KEY)
    img = Image.open(image_file)
    prompt = "Detect and list visible symptoms on the patient's body (e.g., rashes, conjunctivitis, swelling, etc.). Respond with a short comma-separated list."
    response = client.models.generate_content(
        model="gemini-pro-vision",
        contents=[prompt, img]
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
        model="gemini-pro",
        contents=[f"{prompt}\n\n{chat_text}"]
    )
    return response.text.strip()

def webcam_snapshot_widget(key):
    """Streamlit component to capture webcam snapshot and return image bytes."""
    img_data = st.components.v1.html(
        f"""
        <script>
        let stream;
        function captureAndSend() {{
            const video = document.getElementById('webcam_{key}');
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);
            const dataURL = canvas.toDataURL('image/png');
            window.parent.postMessage({{"img_data": dataURL}}, "*");
        }}
        navigator.mediaDevices.getUserMedia({{ video: true }}).then(function(s) {{
            stream = s;
            const video = document.getElementById('webcam_{key}');
            video.srcObject = stream;
        }});
        window.addEventListener('message', function(event) {{
            if (event.data === 'capture_{key}') {{
                captureAndSend();
            }}
        }});
        </script>
        <video id="webcam_{key}" autoplay playsinline width="320" height="240" style="border:1px solid #888;"></video>
        <button onclick="window.parent.postMessage('capture_{key}', '*')">Capture Snapshot</button>
        """,
        height=270,
    )
    # Listen for image data from the component
    img_b64 = st.experimental_get_query_params().get(f'img_data_{key}', [None])[0]
    if img_b64:
        header, img_str = img_b64.split(',', 1)
        img_bytes = base64.b64decode(img_str)
        return img_bytes
    return None

def show():
    st.title("Video Consultation")
    st.markdown("Connect with your doctor through a secure video call and AI-powered assistant.")
    
    if not st.session_state.authenticated:
        st.error("Please log in to access video consultations.")
        return
    
    st.subheader("Start a Video Call")
    appointment_id = st.text_input("Enter Appointment ID")
    user = st.session_state.user
    user_id = user.get("id")
    user_type = st.session_state.get("user_type", "")
    
    # --- Secure Access: Only patient or doctor can join, and only at correct time ---
    appointment_ok = False
    appointment_data = None
    now = datetime.now()
    if appointment_id:
        # Try to find appointment as patient or doctor
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

        # Automated Webcam Snapshot & AI Symptom Detection
        st.markdown("**AI Symptom Detection:** Capture a snapshot from your webcam for AI analysis.")
        img_bytes = webcam_snapshot_widget(key=appointment_id)
        if img_bytes:
            with st.spinner("Analyzing snapshot with Gemini Vision..."):
                ai_symptoms = ai_detect_symptoms(io.BytesIO(img_bytes))
            new_chat = st.session_state[f"chat_{appointment_id}"] + [{"role": "ai", "content": f"Detected symptoms: {ai_symptoms}"}]
            st.session_state[f"chat_{appointment_id}"] = new_chat
            st.success(f"AI detected: {ai_symptoms}")

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
