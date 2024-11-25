"""Data management module for handling CSV data operations."""
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional

class DataManager:
    def __init__(self, config: Dict[str, Any]):
        """Initialize DataManager with configuration."""
        self.config = config
        self.data_path = config["DATA_PATH"]

    def load_data(self) -> pd.DataFrame:
        """Load and validate data from CSV."""
        try:
            df = pd.read_csv(
                self.data_path,
                encoding="utf-8",
                engine='python',
                on_bad_lines='skip'
            )
            
            # Clean column names
            df.columns = [col.strip() for col in df.columns]
            
            # Clean string columns
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].fillna('').astype(str).str.strip()
            
            return df
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return pd.DataFrame()
    
    def save_data(self, df: pd.DataFrame) -> bool:
        """Save data to CSV."""
        try:
            df.to_csv(self.data_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            return False
    
    def get_filtered_data(self, filter_col: str, filter_value: str) -> pd.DataFrame:
        """Get data filtered by column value."""
        df = self.load_data()
        return df[df[filter_col].str.lower() == filter_value.lower()].copy()
    
    def update_records(self, updated_df: pd.DataFrame, id_column: str = "id") -> bool:
        """Update records in the main dataset."""
        try:
            main_df = self.load_data()
            for _, row in updated_df.iterrows():
                main_df.loc[main_df[id_column] == row[id_column]] = row
            return self.save_data(main_df)
        except Exception as e:
            print(f"Error updating records: {str(e)}")
            return False