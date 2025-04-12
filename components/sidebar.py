import streamlit as st
from utils.auth import logout, check_authentication

def render_sidebar():
    with st.sidebar:
        st.title("MedAI")
        st.image("static/images/doctors-animate.svg", width=200)
        
        if check_authentication():
            st.write(f"Welcome, {st.session_state.user['username']}!")
            st.subheader("Navigation")
            
            if st.button("Home"):
                st.session_state.current_page = 'home'
                st.rerun()
            
            if st.session_state.user_type == 'patient':
                if st.button("My Dashboard"):
                    st.session_state.current_page = 'patient_dashboard'
                    st.rerun()
                
                if st.button("Book Appointment"):
                    st.session_state.current_page = 'appointment'
                    st.rerun()
                
                if st.button("Disease Predictor"):
                    st.session_state.current_page = 'disease_predictor'
                    st.rerun()
                
            elif st.session_state.user_type == 'doctor':
                if st.button("My Dashboard"):
                    st.session_state.current_page = 'doctor_dashboard'
                    st.rerun()
                
                if st.button("View Appointments"):
                    st.session_state.current_page = 'doctor_appointments'
                    st.rerun()
                
            elif st.session_state.user_type == 'admin':
                if st.button("Admin Dashboard"):
                    st.session_state.current_page = 'admin_dashboard'
                    st.rerun()
            
            if st.button("Blogs"):
                st.session_state.current_page = 'blog'
                st.rerun()
                
            if st.button("Scans"):
                st.session_state.current_page = 'scans'
                st.rerun()
                
            if st.button("Video Call"):
                st.session_state.current_page = 'video_call'
                st.rerun()
            
            # Logout button
            if st.button("Logout"):
                logout()
                st.rerun()
                
        else:
            st.info("Please login or register to access all features")
