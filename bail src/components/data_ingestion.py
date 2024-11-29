import pandas as pd

class DataIngestion:
  @staticmethod
  def load_data(file_path: str) -> pd.DataFrame:
    """
    Load the dataset from the given file path.
    Args:
        file_path (str): Path to the dataset file.
    Returns:
        pd.DataFrame: Loaded dataset.
    """
    try:
      df = pd.read_csv(file_path)
      print("Data loaded successfully.")
      return df
    except Exception as e:
      raise FileNotFoundError(f"Error loading data from {file_path}: {e}")