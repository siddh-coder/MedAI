import streamlit as st
from utils.database import get_patient_appointments, get_user_by_id

def show():
    st.title("Patient Dashboard")
    user = st.session_state.user
    
    st.header(f"Welcome, {user['username']}")
    st.markdown("Manage your appointments and health information here.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Your Appointments")
        appointments = get_patient_appointments(user['id'])
        
        if not appointments:
            st.info("No appointments scheduled yet.")
        else:
            for apt in appointments:
                with st.expander(f"Appointment with Dr. {apt['doctor_name']} - {apt['date']}"):
                    st.write(f"**Specialization**: {apt['doctor_specialization']}")
                    st.write(f"**Time**: {apt['time']}")
                    st.write(f"**Symptoms**: {apt['symptoms']}")
                    st.write(f"**Status**: {apt['status'].capitalize()}")
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("Book New Appointment", key="book_apt"):
            st.session_state.current_page = 'appointment'
            st.rerun()
        if st.button("Predict Disease", key="predict_disease"):
            st.session_state.current_page = 'disease_predictor'
            st.rerun()
        if st.button("View Blogs", key="view_blogs"):
            st.session_state.current_page = 'blog'
            st.rerun()
        
        st.subheader("Profile")
        user_data = get_user_by_id(user['id'])
        st.write(f"**Email**: {user_data['email']}")
        st.write(f"**Joined**: {user_data['created_at'].strftime('%Y-%m-%d')}")
