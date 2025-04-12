import streamlit as st
from utils.auth import login_user, register_user
import time

def show():
    st.title("Welcome to MedAI")
    st.write("""
    MedAI is a healthcare management system that aims to assist patients in obtaining 
    the necessary medical care for their needs. Register as a patient or doctor, book appointments, 
    and use our disease prediction feature based on symptoms.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Login")
        with st.form("login_form"):
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            login_submit = st.form_submit_button("Login")
            
            if login_submit:
                if not login_email or not login_password:
                    st.error("Please fill in all fields")
                else:
                    success, result = login_user(login_email, login_password)
                    if success:
                        st.success("Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(result)
    
    with col2:
        st.header("Register")
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            user_type = st.selectbox("Register as", ["patient", "doctor"])
            
            # Additional fields for doctors
            additional_info = {}
            if user_type == "doctor":
                specialization = st.text_input("Specialization")
                experience = st.number_input("Years of Experience", min_value=0, value=0)
                qualification = st.text_input("Qualification")
                additional_info = {
                    "specialization": specialization,
                    "experience": experience,
                    "qualification": qualification
                }
            
            register_submit = st.form_submit_button("Register")
            
            if register_submit:
                if not username or not email or not password or not confirm_password:
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, result = register_user(username, email, password, user_type, additional_info)
                    if success:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error(result)
    
    st.header("Features")
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.subheader("🩺 Appointment Booking")
        st.write("Book appointments with qualified doctors based on your medical needs.")
    
    with feature_col2:
        st.subheader("🔍 Disease Prediction")
        st.write("Get preliminary disease predictions based on your symptoms.")
    
    with feature_col3:
        st.subheader("💊 Health Resources")
        st.write("Access informative blogs and resources about various health topics.")
