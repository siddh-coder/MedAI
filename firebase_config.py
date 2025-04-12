import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
def initialize_firebase():
    if not firebase_admin._apps:
        try:
            if "FIREBASE" in st.secrets:
                # Use secrets from Streamlit Cloud
                firebase_creds = st.secrets["FIREBASE"]
                cred = credentials.Certificate(dict(firebase_creds))
                st.info("Initialized Firebase from Streamlit secrets.")
            else:
                # Fallback to local file (for local development)
                service_account_path = "service-account-key.json"
                if not os.path.exists(service_account_path):
                    st.error("Firebase service account key not found. Please add 'service-account-key.json' or define FIREBASE in Streamlit secrets.")
                    st.stop()
                cred = credentials.Certificate(service_account_path)
                st.info("Initialized Firebase from local file.")

            firebase_admin.initialize_app(cred)

        except Exception as e:
            #st.error(f"Error initializing Firebase: {str(e)}")
            service_account_path = "service-account-key.json"
            if not os.path.exists(service_account_path):
                st.error("Firebase service account key not found. Please add 'service-account-key.json' or define FIREBASE in Streamlit secrets.")
                st.stop()
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)

    return firestore.client()

def get_db():
    return initialize_firebase()

