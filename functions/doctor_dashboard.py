import streamlit as st
from utils.database import get_doctor_appointments, get_user_by_id, update_appointment_status

def show():
    st.title("Doctor Dashboard")
    user = st.session_state.user
    
    st.header(f"Welcome, Dr. {user['username']}")
    st.markdown("Manage your appointments and patient interactions here.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Your Appointments")
        appointments = get_doctor_appointments(user['id'])
        
        if not appointments:
            st.info("No appointments scheduled.")
        else:
            for apt in appointments:
                with st.expander(f"Appointment with {apt['patient_name']} - {apt['date']}"):
                    st.write(f"Appointment ID: {apt['id']}")
                    st.write(f"**Time**: {apt['time']}")
                    st.write(f"**Symptoms**: {apt['symptoms']}")
                    st.write(f"**Status**: {apt['status'].capitalize()}")
                    status = st.selectbox(
                        "Update Status",
                        ["pending", "confirmed", "completed", "cancelled"],
                        index=["pending", "confirmed", "completed", "cancelled"].index(apt['status']),
                        key=f"status_{apt['id']}"
                    )
                    if st.button("Update", key=f"update_{apt['id']}"):
                        update_appointment_status(apt['id'], status)
                        st.success("Status updated!")
                        st.rerun()
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("View Blogs", key="doctor_blogs"):
            st.session_state.current_page = 'blog'
            st.rerun()
        if st.button("Join Video Call", key="doctor_video"):
            st.session_state.current_page = 'video_call'
            st.rerun()
        
        st.subheader("Profile")
        user_data = get_user_by_id(user['id'])
        st.write(f"**Specialization**: {user_data.get('specialization', 'N/A')}")
        st.write(f"**Experience**: {user_data.get('experience', 0)} years")
        st.write(f"**Qualification**: {user_data.get('qualification', 'N/A')}")
