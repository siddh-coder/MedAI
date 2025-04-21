# MedAI: AI-Powered Healthcare Platform

![image](https://github.com/user-attachments/assets/00f94065-b88f-4bf0-b539-0c9e1cd9471d)


## Overview
MedAI is a comprehensive, AI-powered healthcare management and telemedicine platform designed for patients, doctors, and administrators. Built for the 2025 Hackathon, MedAI leverages advanced AI models (Google Gemini, HuggingFace) and deep learning to enhance diagnosis, streamline consultations, and empower users with actionable health insights.

---

## Key Features

### 1. Secure Video Consultation with AI Assistance
- Video Calls: Patients and doctors connect via secure Jitsi-powered video calls.
- Live Chat: Real-time chat during consultations, with session-aware input management.
- Webcam Symptom Detection: Capture snapshots during calls; AI (Gemini Vision) detects visible symptoms (e.g., rashes, swelling).
- Meeting Summarization: Gemini AI summarizes chat and findings, extracting diagnosis, medicines, and next steps for medical records.

### 2. Medical Report Analysis (AI)
- Upload Reports: Patients upload PDFs or images of medical reports.
- Gemini AI Analysis: Suggests relevant doctor specializations and explains reasoning.
- Direct Appointment Booking: Book recommended specialists instantly.

### 3. Medical Scans & AI Inference
- Brain Tumor MRI: Upload MRI scans; deep learning model classifies tumor type.
- Cataract Detection: Eye scans analyzed for cataract presence.
- Chest X-Ray (PneumaScan): Integrated link to [PneumaScan](https://pneumascan.streamlit.app) for AI-powered pneumonia detection.

### 4. Disease Prediction
- Symptom-Based Prediction: Select symptoms, get AI-driven disease predictions (using classical ML models).

### 5. Health Blogs & Resources
- Community Blog: Doctors/admins post articles; patients explore curated health content.

### 6. Patient & Doctor Dashboards
- Personalized Dashboards: Manage appointments, view history, access AI tools.
- Profile Management: Update personal and professional details.

### 7. Admin Dashboard
- User & Doctor Management: Approve doctors, manage users, view analytics.
- System Analytics: Metrics on users, doctors, appointments.

### 8. Chatbot (HuggingFace)
- Medical Q&A: AI chatbot answers health queries, logs chat history.

---

## Tech Stack
- Frontend & App Framework: [Streamlit](https://streamlit.io)
- AI/ML: Google Gemini API (Vision & Text), HuggingFace, TensorFlow/Keras (custom models)
- Database: Firebase Firestore
- Authentication: Custom (with Firebase)
- Deployment: Streamlit Cloud / Local

---

## Project Structure
```
MedAI/
├── app.py                     # Main Streamlit entrypoint
├── requirements.txt           # Python dependencies
├── firebase_config.py         # Firebase setup
├── service-account-key.json   # Firebase credentials (secure!)
├── static/                    # Static files (CSS, images)
├── models/
│   ├── csv/                   # Training data for disease prediction
│   └── pkl/                   # Pretrained ML/DL models
├── utils/                     # Helper modules (auth, db, chatbot, etc)
├── functions/                 # All Streamlit page logic
│   ├── home.py
│   ├── patient_dashboard.py
│   ├── doctor_dashboard.py
│   ├── admin_dashboard.py
│   ├── appointment.py
│   ├── disease_predictor.py
│   ├── blog.py
│   ├── scans.py
│   ├── video_call.py
│   ├── patient_report_analysis.py
│   ├── history.py
│   └── chatbot.py
└── ...
```

---

## Security & Privacy
- Authentication: All sensitive features require user login.
- Session Management: Secure session state for user context.
- Data Privacy: Medical data is never shared outside the platform. API keys are stored securely.

---

## Open Source AI Models Used

This project utilizes several open source AI models and APIs, especially from Hugging Face, to power its medical features:

### 1. Disease Prediction (Allopathic)
- **Model:** Custom-trained Scikit-learn model (see `models/pkl/disease_prediction_model.pkl`)
- **Usage:** Predicts probable diseases based on user symptoms.

### 2. Medical Chatbot & LLM-based Inference
- **Model:** [`aaditya/Llama3-OpenBioLLM-70B`](https://huggingface.co/aaditya/Llama3-OpenBioLLM-70B) (via Hugging Face Inference API)
- **Usage:**
  - Medical Q&A Chatbot
  - Ayurveda/Homeopathic diagnosis suggestions
- **API Endpoint:** `https://router.huggingface.co/nebius/v1/chat/completions`
- **Integration:** Used in `functions/chatbot.py`, `functions/disease_predictor.py`, and `utils/chatbot.py`.

### 3. Hugging Face API Key
- Users are prompted to provide their Hugging Face API key for LLM-powered features.

---

**If you use or extend this project, please credit the original model authors and Hugging Face!**

---

## Getting Started
### 1. Clone the Repository
```bash
git clone https://github.com/siddh-coder/MedAI.git
cd MedAI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Firebase
- Place your Firebase `service-account-key.json` in the root directory.
- Configure your Firebase project in `firebase_config.py`.

### 4. Configure API Keys
- Add your Google Gemini API key to Streamlit secrets:
  - In `.streamlit/secrets.toml`:
    ```toml
    GEMINI_API_KEY = "your-gemini-key"
    ```
- (Optional) Add HuggingFace API key for chatbot:
    ```toml
    HF_API_KEY = "your-hf-key"
    ```

### 5. Run the App
```bash
streamlit run app.py
```

---

## AI & ML Models
- Gemini API: Used for text and vision-based inference (symptom detection, summarization, report analysis).
- Custom Models: Brain tumor and cataract detection models (Keras/TensorFlow, stored in `models/pkl/`).
- Disease Prediction: Classical ML model using symptom data (`models/csv/Training.csv`).

---

## Hackathon Innovations
- Seamless AI Integration: Real-time AI feedback during video calls.
- Multi-Modal Analysis: Text, image, and chat data fused for holistic insights.
- Cross-App Linking: PneumaScan integration for advanced pneumonia detection.
- User-Centric Design: Intuitive dashboards for every user type.

---

## Documentation & Support
- Code: Well-commented, modular Python (see `functions/` and `utils/`).
- Issues: Use GitHub Issues for bugs/feature requests.

---

## Contributors
- Siddharth Tripathi(IMT2024011) (Lead Developer)
- [Add other contributors here]

---

## License
This project is for hackathon/demo purposes. Contact the authors for production/commercial use.

---

## Acknowledgements
- Google for Gemini API
- HuggingFace
- Streamlit
- Firebase
- All open-source contributors

---

**Good luck, judges! Explore MedAI and experience the future of AI-driven healthcare.**
