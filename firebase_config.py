import firebase_admin
from firebase_admin import credentials, firestore
import os
import streamlit as st

def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # Always use local service account file for development
            service_account_path = "service-account-key.json"
            if not os.path.exists(service_account_path):
                st.error("Firebase service account key not found. Please place it in the root directory.")
                st.stop()
            cred = credentials.Certificate(service_account_path)
            
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Error initializing Firebase: {str(e)}")
            st.stop()
    
    return firestore.client()

def get_db():
    return initialize_firebase()
