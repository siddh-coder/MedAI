import streamlit as st
from utils.auth import logout, check_authentication

def render_sidebar():
    with st.sidebar:
        st.title("MedAI")
        st.image("static/images/doctors-animate.svg", width=200)
        
        if check_authentication():
            st.write(f"Welcome, {st.session_state.user['username']}!")
            st.subheader("Navigation")
            
            if st.button("Home", key="sidebar_home"):
                st.session_state.current_page = 'home'
                st.rerun()
            
            if st.session_state.user_type == 'patient':
                if st.button("My Dashboard", key="sidebar_patient_dashboard"):
                    st.session_state.current_page = 'patient_dashboard'
                    st.rerun()
                if st.button("Book Appointment", key="sidebar_appointment"):
                    st.session_state.current_page = 'appointment'
                    st.rerun()
                if st.button("Disease Predictor", key="sidebar_disease_predictor"):
                    st.session_state.current_page = 'disease_predictor'
                    st.rerun()
                if st.button("Medical Report Analysis", key="sidebar_patient_report_analysis"):
                    st.session_state.current_page = 'patient_report_analysis'
                    st.rerun()
                if st.button("History", key="sidebar_history"):
                    st.session_state.current_page = 'history'
                    st.rerun()
                if st.button("Chatbot", key="sidebar_chatbot"):
                    st.session_state.current_page = 'chatbot'
                    st.rerun()
            
            elif st.session_state.user_type == 'doctor':
                if st.button("My Dashboard", key="sidebar_doctor_dashboard"):
                    st.session_state.current_page = 'doctor_dashboard'
                    st.rerun()
                if st.button("View Appointments", key="sidebar_doctor_appointments"):
                    st.session_state.current_page = 'appointment'
                    st.rerun()
                if st.button("History", key="sidebar_history_doctor"):
                    st.session_state.current_page = 'history'
                    st.rerun()
                if st.button("Chatbot", key="sidebar_chatbot_doctor"):
                    st.session_state.current_page = 'chatbot'
                    st.rerun()
            
            elif st.session_state.user_type == 'admin':
                if st.button("Admin Dashboard", key="sidebar_admin_dashboard"):
                    st.session_state.current_page = 'admin_dashboard'
                    st.rerun()
                if st.button("History", key="sidebar_history_admin"):
                    st.session_state.current_page = 'history'
                    st.rerun()
                if st.button("Chatbot", key="sidebar_chatbot_admin"):
                    st.session_state.current_page = 'chatbot'
                    st.rerun()
            
            if st.button("Blogs", key="sidebar_blog"):
                st.session_state.current_page = 'blog'
                st.rerun()
                
            if st.button("Scans", key="sidebar_scans"):
                st.session_state.current_page = 'scans'
                st.rerun()
                
            if st.button("Video Call", key="sidebar_video_call"):
                st.session_state.current_page = 'video_call'
                st.rerun()
            
            if st.button("Privacy Policy", key="sidebar_privacy"):
                st.session_state.current_page = 'privacy_policy'
                st.rerun()
            
            if st.button("Logout", key="sidebar_logout"):
                logout()
                st.rerun()
        else:
            st.info("Please login or register to access all features")
