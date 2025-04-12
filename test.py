import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

st.set_page_config(page_title="Firebase Connection Test")

# Check if Firebase is already initialized
if not firebase_admin._apps:
    try:
        # Path to your service account key
        service_account_path = "service-account-key.json"
        
        # Display service account details (with sensitive info hidden)
        if os.path.exists(service_account_path):
            with open(service_account_path, 'r') as f:
                creds = json.load(f)
                project_id = creds.get('project_id', 'Unknown')
                st.success(f"Found service account file for project: {project_id}")
        else:
            st.error("Service account key file not found!")
            st.stop()
            
        # Initialize Firebase
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
        st.success("Firebase successfully initialized!")
    except Exception as e:
        st.error(f"Error initializing Firebase: {str(e)}")
        st.stop()

# Get Firestore client
try:
    db = firestore.client()
    st.success("Firestore client created successfully!")
    
    # Test writing to Firestore
    if st.button("Test Database Write"):
        doc_ref = db.collection('test').document('test_doc')
        doc_ref.set({
            'timestamp': firestore.SERVER_TIMESTAMP,
            'message': 'Hello from Streamlit!'
        })
        st.success("Successfully wrote to Firestore!")
    
    # Test reading from Firestore
    if st.button("Test Database Read"):
        docs = db.collection('test').limit(10).get()
        
        if docs:
            st.write("Recent test documents:")
            for doc in docs:
                st.write(f"Document ID: {doc.id}")
                st.write(doc.to_dict())
        else:
            st.info("No test documents found. Try writing to the database first.")
            
except Exception as e:
    st.error(f"Error connecting to Firestore: {str(e)}")
