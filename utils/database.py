from firebase_config import get_db
from datetime import datetime

db = get_db()

def get_user_by_id(user_id):
    user_doc = db.collection('users').document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        user_data['id'] = user_id
        return user_data
    return None

def get_doctors():
    doctors = []
    docs = db.collection('users').where('user_type', '==', 'doctor').get()
    for doc in docs:
        doctor_data = doc.to_dict()
        doctor_data['id'] = doc.id
        doctors.append(doctor_data)
    return doctors

def create_appointment(patient_id, doctor_id, date, time, symptoms, status="pending"):
    appointment_data = {
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'date': date,
        'time': time,
        'symptoms': symptoms,
        'status': status,
        'created_at': datetime.now()
    }
    appointment_ref = db.collection('appointments').add(appointment_data)
    return appointment_ref[1].id

def get_patient_appointments(patient_id):
    appointments = []
    docs = db.collection('appointments').where('patient_id', '==', patient_id).order_by('date').get()
    for doc in docs:
        apt_data = doc.to_dict()
        apt_data['id'] = doc.id
        doctor = get_user_by_id(apt_data['doctor_id'])
        if doctor:
            apt_data['doctor_name'] = doctor['username']
            apt_data['doctor_specialization'] = doctor.get('specialization', 'General')
        appointments.append(apt_data)
    return appointments

def get_doctor_appointments(doctor_id):
    appointments = []
    docs = db.collection('appointments').where('doctor_id', '==', doctor_id).order_by('date').get()
    for doc in docs:
        apt_data = doc.to_dict()
        apt_data['id'] = doc.id
        patient = get_user_by_id(apt_data['patient_id'])
        if patient:
            apt_data['patient_name'] = patient['username']
        appointments.append(apt_data)
    return appointments

def update_appointment_status(appointment_id, status):
    db.collection('appointments').document(appointment_id).update({
        'status': status,
        'updated_at': datetime.now()
    })
    return True

def update_user_profile(user_id, profile_data):
    db.collection('users').document(user_id).update({
        **profile_data,
        'updated_at': datetime.now()
    })
    return True

def add_blog_post(title, content, author_id, category):
    blog_data = {
        'title': title,
        'content': content,
        'author_id': author_id,
        'category': category,
        'created_at': datetime.now(),
        'views': 0
    }
    blog_ref = db.collection('blogs').add(blog_data)
    return blog_ref[1].id

def get_blog_posts(category=None, limit=10):
    blogs = []
    if category:
        query = db.collection('blogs').where('category', '==', category).order_by('created_at', direction='DESCENDING').limit(limit).get()
    else:
        query = db.collection('blogs').order_by('created_at', direction='DESCENDING').limit(limit).get()
    for doc in query:
        blog_data = doc.to_dict()
        blog_data['id'] = doc.id
        author = get_user_by_id(blog_data['author_id'])
        if author:
            blog_data['author_name'] = author['username']
        blogs.append(blog_data)
    return blogs

def increment_blog_views(blog_id):
    db.collection('blogs').document(blog_id).update({
        'views': firestore.Increment(1)
    })

def modify_appointment(appointment_id, date, time, symptoms):
    db.collection('appointments').document(appointment_id).update({
        'date': date,
        'time': time,
        'symptoms': symptoms,
        'updated_at': datetime.now()
    })
    return True

def save_prescription(appointment_id, doctor_id, prescription):
    """
    Save prescription text for both doctor and patient for a given appointment.
    """
    # Fetch appointment to get patient_id
    apt_doc = db.collection('appointments').document(appointment_id).get()
    if not apt_doc.exists:
        return False
    apt_data = apt_doc.to_dict()
    patient_id = apt_data.get('patient_id')
    # Save prescription in a subcollection for both doctor and patient
    presc_data = {
        'appointment_id': appointment_id,
        'doctor_id': doctor_id,
        'patient_id': patient_id,
        'prescription': prescription,
        'created_at': datetime.now()
    }
    # For doctor
    db.collection('users').document(doctor_id).collection('prescriptions').add(presc_data)
    # For patient
    db.collection('users').document(patient_id).collection('prescriptions').add(presc_data)
    # Optionally, attach prescription to appointment
    db.collection('appointments').document(appointment_id).update({'prescription': prescription, 'prescription_created_at': datetime.now()})
    return True
