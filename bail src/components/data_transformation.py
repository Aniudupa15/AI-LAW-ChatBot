from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd

class DataTransformation:
  def __init__(self):
    self.label_encoders = {}
    self.scaler = StandardScaler()
  
  def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Fit and transform the dataset.
    Args:
        df (pd.DataFrame): Original dataset.
    Returns:
        pd.DataFrame: Preprocessed dataset.
    """
    try:
      # Encode categorical columns
      categorical_columns = ['statute', 'offense_category', 'penalty']
      for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        self.label_encoders[col] = le
      
      # Convert boolean columns to integers
      boolean_columns = [
        'risk_of_escape', 'risk_of_influence', 'surety_bond_required',
        'personal_bond_required', 'fines_applicable', 'served_half_term'
      ]
      df[boolean_columns] = df[boolean_columns].astype(int)

      # Scale numerical columns
      numerical_columns = ['imprisonment_duration_served', 'risk_score', 'penalty_severity']
      df[numerical_columns] = self.scaler.fit_transform(df[numerical_columns])
      
      print("Data transformation completed.")
      return df
    except Exception as e:
      raise RuntimeError(f"Error during data transformation: {e}")