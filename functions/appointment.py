import streamlit as st
from utils.database import get_doctors, create_appointment, get_patient_appointments, update_appointment_status, modify_appointment
from datetime import datetime, timedelta

def show():
    st.title("Appointment Booking")
    
    if st.session_state.user_type != 'patient':
        st.error("Only patients can book appointments.")
        return
    
    user = st.session_state.user
    st.header("Book a New Appointment")
    
    try:
        doctors = get_doctors()
    except Exception as e:
        st.error(f"Failed to fetch doctors: {e}")
        doctors = []
    
    if not doctors:
        st.warning("No doctors available at the moment.")
        return
    
    doctor_options = {f"Dr. {d['username']} ({d.get('specialization', 'General')})": d['id'] for d in doctors}
    reverse_doctor_options = {v: k for k, v in doctor_options.items()}
    default_doctor = None
    if 'selected_doctor_id' in st.session_state and st.session_state.selected_doctor_id in reverse_doctor_options:
        default_doctor = reverse_doctor_options[st.session_state.selected_doctor_id]
    selected_doctor = st.selectbox("Select Doctor", list(doctor_options.keys()), index=list(doctor_options.keys()).index(default_doctor) if default_doctor else 0)
    date = st.date_input("Select Date", min_value=datetime.now().date())
    time = st.time_input("Select Time")
    symptoms = st.text_area("Describe Your Symptoms")
    
    # Store appointment id after booking
    if 'last_appointment_id' not in st.session_state:
        st.session_state['last_appointment_id'] = None
    
    if st.button("Book Appointment"):
        if not symptoms:
            st.error("Please describe your symptoms.")
        else:
            doctor_id = doctor_options[selected_doctor]
            try:
                appointment_id = create_appointment(
                    patient_id=user['id'],
                    doctor_id=doctor_id,
                    date=date.strftime('%Y-%m-%d'),
                    time=time.strftime('%H:%M'),
                    symptoms=symptoms
                )
                st.session_state['last_appointment_id'] = appointment_id
                st.success(f"Appointment booked successfully! Your Appointment ID: {appointment_id}")
            except Exception as e:
                st.error(f"Failed to book appointment: {e}")
            if 'selected_doctor_id' in st.session_state:
                del st.session_state.selected_doctor_id
            st.session_state['modify_open'] = None
            st.rerun()
    
    if st.session_state.get('last_appointment_id'):
        st.info(f"Your last booked Appointment ID: {st.session_state['last_appointment_id']}")
    
    st.subheader("Your Upcoming Appointments")
    try:
        appointments = get_patient_appointments(user['id'])
    except Exception as e:
        st.error(f"Could not fetch appointments: {e}")
        appointments = []
    
    if not appointments:
        st.info("No upcoming appointments.")
    else:
        modify_open = st.session_state.get('modify_open', None)
        for apt in appointments:
            with st.expander(f"Appointment with Dr. {apt.get('doctor_name', 'Unknown')} - {apt['date']}"):
                st.write(f"**Appointment ID:** `{apt.get('id', 'N/A')}`")
                st.write(f"**Specialization**: {apt.get('doctor_specialization', 'General')}")
                st.write(f"**Time**: {apt['time']}")
                st.write(f"**Symptoms**: {apt['symptoms']}")
                st.write(f"**Status**: {apt['status'].capitalize()}")
                if apt['status'] == 'pending':
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Cancel", key=f"cancel_{apt['id']}"):
                            try:
                                update_appointment_status(apt['id'], 'cancelled')
                                st.success("Appointment cancelled.")
                            except Exception as e:
                                st.error(f"Failed to cancel appointment: {e}")
                            st.session_state['modify_open'] = None
                            st.rerun()
                    with col2:
                        if st.button("Modify", key=f"modify_{apt['id']}"):
                            if modify_open is None:
                                st.session_state['modify_open'] = apt['id']
                                st.rerun()
                            else:
                                st.error("Please close the other modify form first.")
                    if modify_open == apt['id']:
                        new_date = st.date_input("New Date", value=datetime.strptime(apt['date'], '%Y-%m-%d').date(), key=f"date_{apt['id']}")
                        new_time = st.time_input("New Time", value=datetime.strptime(apt['time'], '%H:%M').time(), key=f"time_{apt['id']}")
                        new_symptoms = st.text_area("Update Symptoms", value=apt['symptoms'], key=f"symptoms_{apt['id']}")
                        if st.button("Save Changes", key=f"save_{apt['id']}"):
                            try:
                                modify_appointment(apt['id'], new_date.strftime('%Y-%m-%d'), new_time.strftime('%H:%M'), new_symptoms)
                                st.success("Appointment modified.")
                            except Exception as e:
                                st.error(f"Failed to modify appointment: {e}")
                            st.session_state['modify_open'] = None
                            st.rerun()
