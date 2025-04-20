import streamlit as st
import firebase_admin
from firebase_config import get_db
from utils.auth import check_authentication
from components.sidebar import render_sidebar
from functions import (
    home, patient_dashboard, doctor_dashboard, admin_dashboard,
    appointment, disease_predictor, blog, scans, video_call, patient_report_analysis, history, chatbot
)

st.set_page_config(
    page_title="MedAI - Healthcare Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

db = get_db()

def init_session_state():
    defaults = {
        'user': None,
        'user_type': None,
        'authenticated': False,
        'current_page': 'home',
        'theme': 'light'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def main():
    init_session_state()
    
    with open('static/css/style.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    render_sidebar()
    
    page_map = {
        'home': home,
        'patient_dashboard': patient_dashboard,
        'doctor_dashboard': doctor_dashboard,
        'admin_dashboard': admin_dashboard,
        'appointment': appointment,
        'disease_predictor': disease_predictor,
        'blog': blog,
        'scans': scans,
        'video_call': video_call,
        'patient_report_analysis': patient_report_analysis,
        'history': history,
        'chatbot': chatbot
    }
    
    if not check_authentication():
        home.show()
    else:
        current_page = st.session_state.current_page
        if current_page in page_map:
            page_map[current_page].show()
        else:
            st.error("Page not found")
            home.show()

if __name__ == "__main__":
    main()
