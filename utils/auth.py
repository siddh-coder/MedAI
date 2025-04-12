import streamlit as st
import bcrypt
from firebase_config import get_db
import re
from datetime import datetime

db = get_db()

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def register_user(username, email, password, user_type, additional_info=None):
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', email).limit(1).get()
    
    if len(query) > 0:
        return False, "Email already registered"

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email format"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    user_data = {
        'username': username,
        'email': email,
        'password': hash_password(password),
        'user_type': user_type,
        'created_at': datetime.now(),
    }
    
    if user_type == 'doctor' and additional_info:
        user_data.update(additional_info)
    
    user_ref = users_ref.add(user_data)
    
    return True, user_ref[1].id

def login_user(email, password):
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', email).limit(1).get()
    
    if not query:
        return False, "Email not found"
    
    user_doc = query[0]
    user_data = user_doc.to_dict()
    
    if verify_password(user_data['password'], password):
        user_info = {
            'id': user_doc.id,
            'username': user_data['username'],
            'email': user_data['email'],
            'user_type': user_data['user_type']
        }
        
        st.session_state.user = user_info
        st.session_state.user_type = user_data['user_type']
        st.session_state.authenticated = True
        
        return True, user_info
    else:
        return False, "Incorrect password"

def check_authentication():
    return st.session_state.authenticated and st.session_state.user is not None

def logout():
    st.session_state.user = None
    st.session_state.user_type = None
    st.session_state.authenticated = False
    st.session_state.current_page = 'home'
