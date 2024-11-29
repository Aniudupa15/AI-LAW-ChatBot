import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.data_ingestion import DataIngestion
from components.data_transformation import DataTransformation
from components.model_trainer import ModelTrainer
from sklearn.model_selection import train_test_split
import joblib

# Load data
data = DataIngestion.load_data('data/a.csv')

# Preprocess data
transformer = DataTransformation()
data = transformer.fit_transform(data)

# Split data
X = data.drop(columns=['case_id', 'bail_eligibility'])
y = data['bail_eligibility']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
trainer = ModelTrainer()
trainer.train(X_train, y_train)

# Evaluate model
trainer.evaluate(X_test, y_test)

# Ensure the models folder exists
models_dir = os.path.join("bail src", "models")
os.makedirs(models_dir, exist_ok=True)

# Save model and preprocessing objects
model_path = os.path.join(models_dir, 'bail_reckoner_model.pkl')
preprocessing_path = os.path.join(models_dir, 'preprocessing_objects.pkl')

trainer.save_model(model_path)
joblib.dump({'label_encoders': transformer.label_encoders, 'scaler': transformer.scaler}, preprocessing_path)