from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from typing import Dict
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Define paths for preprocessing objects and model
preprocessing_path = os.path.join("ipc_vector_db", "preprocessing_objects.pkl")
model_path = os.path.join("ipc_vector_db", "bail_reckoner_model.pkl")

# Load preprocessing objects and model
preprocessing_objects = joblib.load(preprocessing_path)
model = joblib.load(model_path)

label_encoders = preprocessing_objects['label_encoders']
scaler = preprocessing_objects['scaler']

# Define Pydantic model for input data
class BailInput(BaseModel):
    statute: str
    offense_category: str
    penalty: str
    imprisonment_duration_served: int
    risk_of_escape: int
    risk_of_influence: int
    surety_bond_required: int
    personal_bond_required: int
    fines_applicable: int
    served_half_term: int
    risk_score: float
    penalty_severity: float

# Endpoint for prediction
@app.post("/predict-bail")
async def predict_bail(data: BailInput):
    try:
        # Convert input data to DataFrame
        user_input = pd.DataFrame([data.dict()])

        # Preprocess categorical columns
        for col, encoder in label_encoders.items():
            if col in user_input:
                user_input[col] = encoder.transform(user_input[col])

        # Preprocess numerical columns
        numerical_columns = ['imprisonment_duration_served', 'risk_score', 'penalty_severity']
        user_input[numerical_columns] = scaler.transform(user_input[numerical_columns])

        # Predict using the model
        result = model.predict(user_input)

        # Prepare response
        prediction = "Eligible for Bail" if result[0] == 1 else "Not Eligible for Bail"
        return {"prediction": prediction}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
