from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import pandas as pd

class ModelTrainer:
  def __init__(self):
    self.model = RandomForestClassifier(random_state=42, n_estimators=100)
  
  def train(self, X_train: pd.DataFrame, y_train: pd.Series):
    """
    Train the model.
    Args:
      X_train (pd.DataFrame): Training features.
      y_train (pd.Series): Training labels.
    """
    try:
      self.model.fit(X_train, y_train)
      print("Model training completed.")
    except Exception as e:
      raise RuntimeError(f"Error during model training: {e}")

  def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """
    Evaluate the trained model.
    Args:
      X_test (pd.DataFrame): Test features.
      y_test (pd.Series): Test labels.
    """
    try:
      y_pred = self.model.predict(X_test)
      accuracy = accuracy_score(y_test, y_pred)
      report = classification_report(y_test, y_pred)
      
      print(f"Accuracy: {accuracy * 100:.2f}%")
      print("\nClassification Report:\n", report)
    except Exception as e:
      raise RuntimeError(f"Error during model evaluation: {e}")

  def save_model(self, model_path: str):
    """
    Save the trained model to a file.
    Args:
      model_path (str): Path to save the model.
    """
    try:
      joblib.dump(self.model, model_path)
      print(f"Model saved at {model_path}.")
    except Exception as e:
      raise IOError(f"Error saving the model: {e}")