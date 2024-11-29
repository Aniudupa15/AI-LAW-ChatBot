import pandas as pd
import joblib
import os

# Define correct path for preprocessing objects
preprocessing_path = os.path.join("bail src", "models", "preprocessing_objects.pkl")
model_path = os.path.join("bail src", "models", "bail_reckoner_model.pkl")

# Load preprocessing objects and model
preprocessing_objects = joblib.load(preprocessing_path)
model = joblib.load(model_path)

label_encoders = preprocessing_objects['label_encoders']
scaler = preprocessing_objects['scaler']

# Example user input
user_input = pd.DataFrame([{
    'statute': 'NDPS',
    'offense_category': 'Crimes Against Women',
    'penalty': 'Fine',
    'imprisonment_duration_served': 90,
    'risk_of_escape': 1,
    'risk_of_influence': 0,
    'surety_bond_required': 0,
    'personal_bond_required': 1,
    'fines_applicable': 1,
    'served_half_term': 0,
    'risk_score': 4.5,
    'penalty_severity': 2.0
}])

# Preprocess user input
for col, encoder in label_encoders.items():
    user_input[col] = encoder.transform(user_input[col])

numerical_columns = ['imprisonment_duration_served', 'risk_score', 'penalty_severity']
user_input[numerical_columns] = scaler.transform(user_input[numerical_columns])

# Predict
result = model.predict(user_input)
print("Prediction Result:", "Eligible for Bail" if result[0] == 1 else "Not Eligible for Bail")