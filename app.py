import streamlit as st
import firebase_admin
from firebase_config import get_db
import os
from utils.auth import check_authentication, logout
from components.sidebar import render_sidebar
from functions import home, patient_dashboard, doctor_dashboard, admin_dashboard

# Set page configuration
st.set_page_config(
    page_title="MedAI - Healthcare Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database
db = get_db()

# Initialize session state variables if they don't exist
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
    
# Main application
def main():
    # Custom CSS
    with open('static/css/style.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Show appropriate page based on user authentication status and type
    if not st.session_state.authenticated:
        home.show()
    else:
        if st.session_state.current_page == 'home':
            home.show()
        elif st.session_state.user_type == 'patient':
            patient_dashboard.show()
        elif st.session_state.user_type == 'doctor':
            doctor_dashboard.show()
        elif st.session_state.user_type == 'admin':
            admin_dashboard.show()
        else:
            st.error("Unknown user type")

if __name__ == "__main__":
    main()
