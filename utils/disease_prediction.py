import pandas as pd
import numpy as np
import joblib

# Load model and label encoder
model = joblib.load("./models/pkl/disease_prediction_model.pkl")
label_encoder = joblib.load("./models/pkl/label_encoder.pkl")

# Load symptom list
df = pd.read_csv("./models/csv/Training.csv")
symptom_columns = df.columns.drop(["prognosis", *[col for col in df.columns if "Unnamed" in col]])

# Function to predict probabilities of diseases from symptom list
def predict_disease(symptoms):
    input_data = np.zeros(len(symptom_columns))

    for symptom in symptoms:
        if symptom in symptom_columns:
            input_data[symptom_columns.get_loc(symptom)] = 1
        else:
            print(f"Warning: '{symptom}' is not a recognized symptom.")

    # Get probabilities
    probabilities = model.predict_proba([input_data])[0]
    disease_names = label_encoder.inverse_transform(np.arange(len(probabilities)))

    # Combine and sort results
    results = sorted(zip(disease_names, probabilities), key=lambda x: x[1], reverse=True)
    return results[:5]