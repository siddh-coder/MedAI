import streamlit as st

def show():
    st.title("Video Consultation")
    st.markdown("Connect with your doctor through a secure video call.")
    
    if not st.session_state.authenticated:
        st.error("Please log in to access video consultations.")
        return
    
    st.subheader("Start a Video Call")
    appointment_id = st.text_input("Enter Appointment ID")
    
    if st.button("Join Call"):
        if not appointment_id:
            st.error("Please enter a valid Appointment ID.")
        else:
            st.success(f"Joining video call for Appointment ID: {appointment_id}")
            st.markdown("""
            **Note**: Video call functionality requires integration with a third-party service like Agora or Twilio.
            Please ensure your appointment is confirmed and the doctor is available.
            """)
            st.info("Redirecting to video call interface...")
            # Placeholder for video call iframe or external link
            st.markdown('<a href="https://meet.example.com" target="_blank">Join Video Call</a>', unsafe_allow_html=True)
    
    st.subheader("Tips for a Successful Call")
    st.markdown("""
    - Ensure a stable internet connection.
    - Use headphones for better audio quality.
    - Find a quiet, well-lit space for your consultation.
    """)
