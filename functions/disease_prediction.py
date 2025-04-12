import pickle
import numpy as np

def load_model():
    with open('static/data/disease_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

def predict_disease(symptom_input):
    model = load_model()
    symptom_array = np.array([symptom_input])
    prediction = model.predict(symptom_array)[0]
    probabilities = model.predict_proba(symptom_array)[0]
    max_prob = max(probabilities)
    return prediction, max_prob
