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
    docs = db.collection('appointments').where('patient_id', '==', patient_id).get()
    
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
    docs = db.collection('appointments').where('doctor_id', '==', doctor_id).get()
    
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
        'created_at': datetime.now()
    }
    
    blog_ref = db.collection('blogs').add(blog_data)
    return blog_ref[1].id

def get_blog_posts(category=None, limit=10):
    blogs = []
    
    if category:
        query = db.collection('blogs').where('category', '==', category).limit(limit).get()
    else:
        query = db.collection('blogs').limit(limit).get()
    
    for doc in query:
        blog_data = doc.to_dict()
        blog_data['id'] = doc.id
        author = get_user_by_id(blog_data['author_id'])
        if author:
            blog_data['author_name'] = author['username']
        
        blogs.append(blog_data)
    
    return blogs
