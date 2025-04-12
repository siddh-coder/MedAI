import streamlit as st
from utils.database import get_doctors, create_appointment, get_patient_appointments
from datetime import datetime, timedelta

def show():
    st.title("Appointment Booking")
    
    if st.session_state.user_type != 'patient':
        st.error("Only patients can book appointments.")
        return
    
    user = st.session_state.user
    st.header("Book a New Appointment")
    
    doctors = get_doctors()
    if not doctors:
        st.warning("No doctors available at the moment.")
        return
    
    doctor_options = {f"Dr. {d['username']} ({d.get('specialization', 'General')})": d['id'] for d in doctors}
    selected_doctor = st.selectbox("Select Doctor", list(doctor_options.keys()))
    date = st.date_input("Select Date", min_value=datetime.now().date())
    time = st.time_input("Select Time")
    symptoms = st.text_area("Describe Your Symptoms")
    
    if st.button("Book Appointment"):
        if not symptoms:
            st.error("Please describe your symptoms.")
        else:
            doctor_id = doctor_options[selected_doctor]
            create_appointment(
                patient_id=user['id'],
                doctor_id=doctor_id,
                date=date.strftime('%Y-%m-%d'),
                time=time.strftime('%H:%M'),
                symptoms=symptoms
            )
            st.success("Appointment booked successfully!")
            st.rerun()
    
    st.subheader("Your Upcoming Appointments")
    appointments = get_patient_appointments(user['id'])
    
    if not appointments:
        st.info("No upcoming appointments.")
    else:
        for apt in appointments:
            with st.expander(f"Appointment with Dr. {apt['doctor_name']} - {apt['date']}"):
                st.write(f"**Specialization**: {apt['doctor_specialization']}")
                st.write(f"**Time**: {apt['time']}")
                st.write(f"**Symptoms**: {apt['symptoms']}")
                st.write(f"**Status**: {apt['status'].capitalize()}")
                if apt['status'] == 'pending' and st.button("Cancel", key=f"cancel_{apt['id']}"):
                    update_appointment_status(apt['id'], 'cancelled')
                    st.success("Appointment cancelled.")
                    st.rerun()
