import streamlit as st
import pandas as pd
from utils.disease_prediction import predict_disease

def show():
    st.title("Disease Predictor")
    st.markdown("Enter your symptoms to get a preliminary disease prediction using our AI model.")
    
    if st.session_state.user_type != 'patient':
        st.error("This feature is available only to patients.")
        return
    
    symptoms_df = pd.read_csv("static/data/symptoms.csv")
    symptom_columns = [col for col in symptoms_df.columns if col != 'disease']
    
    st.subheader("Select Your Symptoms")
    selected_symptoms = {}
    cols = st.columns(3)
    
    for idx, symptom in enumerate(symptom_columns):
        with cols[idx % 3]:
            selected_symptoms[symptom] = st.checkbox(symptom, key=f"symptom_{symptom}")
    
    if st.button("Predict Disease"):
        if not any(selected_symptoms.values()):
            st.error("Please select at least one symptom.")
        else:
            symptom_input = [1 if selected_symptoms[symptom] else 0 for symptom in symptom_columns]
            prediction, probability = predict_disease(symptom_input)
            
            st.subheader("Prediction Results")
            st.write(f"**Predicted Disease**: {prediction}")
            st.write(f"**Confidence**: {probability:.2%}")
            st.warning("This is a preliminary prediction. Please consult a doctor for an accurate diagnosis.")
            
            with st.expander("Next Steps"):
                st.markdown("""
                - **Book an Appointment**: Schedule a consultation with a doctor.
                - **Learn More**: Check our blog for related health information.
                """)
                if st.button("Book Appointment Now"):
                    st.session_state.current_page = 'appointment'
                    st.rerun()
