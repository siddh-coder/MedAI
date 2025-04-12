import streamlit as st
from utils.database import get_doctors, get_user_by_id

def show():
    st.title("Admin Dashboard")
    
    if st.session_state.user_type != 'admin':
        st.error("Access restricted to admins.")
        return
    
    st.header("System Management")
    
    tabs = st.tabs(["Users", "Doctors", "Analytics"])
    
    with tabs[0]:
        st.subheader("Manage Users")
        users = db.collection('users').get()
        for user in users:
            user_data = user.to_dict()
            user_data['id'] = user.id
            with st.expander(f"{user_data['username']} ({user_data['user_type'].capitalize()})"):
                st.write(f"**Email**: {user_data['email']}")
                st.write(f"**Joined**: {user_data['created_at'].strftime('%Y-%m-%d')}")
                if st.button("Delete User", key=f"delete_{user.id}"):
                    db.collection('users').document(user.id).delete()
                    st.success(f"User {user_data['username']} deleted.")
                    st.rerun()
    
    with tabs[1]:
        st.subheader("Manage Doctors")
        doctors = get_doctors()
        if not doctors:
            st.info("No doctors registered.")
        else:
            for doctor in doctors:
                with st.expander(f"Dr. {doctor['username']}"):
                    st.write(f"**Specialization**: {doctor.get('specialization', 'N/A')}")
                    st.write(f"**Experience**: {doctor.get('experience', 0)} years")
                    st.write(f"**Qualification**: {doctor.get('qualification', 'N/A')}")
    
    with tabs[2]:
        st.subheader("System Analytics")
        user_count = len(db.collection('users').get())
        doctor_count = len(get_doctors())
        appointment_count = len(db.collection('appointments').get())
        st.metric("Total Users", user_count)
        st.metric("Total Doctors", doctor_count)
        st.metric("Total Appointments", appointment_count)
