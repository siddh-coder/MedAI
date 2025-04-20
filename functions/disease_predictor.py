import streamlit as st
import pandas as pd
from utils.disease_prediction import predict_disease
from utils.chatbot import stream_chatbot_response


def show():
    st.title("Disease Predictor")
    st.markdown("Enter your symptoms to get a preliminary disease prediction using our AI model.")
    
    if st.session_state.user_type != 'patient':
        st.error("This feature is available only to patients.")
        return
    
    symptoms_df = pd.read_csv("models/csv/Training.csv")
    symptom_columns = [col for col in symptoms_df.columns if col != 'prognosis']
    
    st.subheader("Select Your Symptoms")
    selected_symptom_names = st.multiselect(
        "Select your symptoms",
        options=symptom_columns,
        help="Start typing to search for symptoms"
    )
    
    st.subheader("Select Inference Type")
    inference_type = st.selectbox(
        "Choose inference method:",
        ["Allopathic (AI)", "Ayurveda (LLM)", "Homeopathic (LLM)"]
    )
    
    api_key = "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"
        
    if st.button("Predict Disease"):
        if not selected_symptom_names:
            st.error("Please select at least one symptom.")
        else:
            if inference_type == "Allopathic (AI)":
                top_diseases = predict_disease(selected_symptom_names)
                st.subheader("Prediction Results (Allopathic)")
                for disease, prob in top_diseases:
                    st.write(f"**{disease}**: {prob:.2%}")
                st.warning("This is a preliminary prediction. Please consult a doctor for an accurate diagnosis.")
            else:
                st.subheader(f"Prediction Results ({inference_type})")
                prompt = f"Given these symptoms: {', '.join(selected_symptom_names)}, provide a {inference_type.lower()} diagnosis and possible remedies."
                messages = [
                    {"role": "user", "content": prompt}
                ]
                placeholder = st.empty()
                if api_key:
                    stream_chatbot_response(messages, api_key, placeholder)
                else:
                    st.info("Please provide your HuggingFace API Key above.")
            
            with st.expander("Next Steps"):
                st.markdown("""
                - **Book an Appointment**: Schedule a consultation with a doctor.
                - **Learn More**: Check our blog for related health information.
                """)
                if st.button("Book Appointment Now"):
                    st.session_state.current_page = 'appointment'
                    st.rerun()
