import streamlit as st

def user_card(username, email, user_type, created_at):
    with st.container():
        st.markdown(f"**{username}** ({user_type.capitalize()})")
        st.write(f"Email: {email}")
        st.write(f"Joined: {created_at.strftime('%Y-%m-%d')}")
        st.divider()

def appointment_card(appointment, role='patient'):
    with st.expander(f"Appointment - {appointment['date']}"):
        if role == 'patient':
            st.write(f"Doctor: Dr. {appointment['doctor_name']}")
            st.write(f"Specialization: {appointment['doctor_specialization']}")
        else:
            st.write(f"Patient: {appointment['patient_name']}")
        st.write(f"Time: {appointment['time']}")
        st.write(f"Symptoms: {appointment['symptoms']}")
        st.write(f"Status: {appointment['status'].capitalize()}")
