import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import datetime

# Initialize Firebase app only once
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["FIREBASE"])
    firebase_admin.initialize_app(cred)
db = firestore.client()

def add_history_entry(user_id, entry_type, data):
    '''Add a new entry to the user's history.'''
    doc_ref = db.collection("user_histories").document(user_id)
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": entry_type,
        **data
    }
    doc_ref.set({"history": firestore.ArrayUnion([entry])}, merge=True)


def get_user_history(user_id):
    '''Fetch the user's history as a list.'''
    doc_ref = db.collection("user_histories").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("history", [])
    return []
