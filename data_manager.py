"""Data management functionality."""
import pandas as pd
from typing import Dict, Any
from data_source import DataSourceManager

class DataManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_source = DataSourceManager(config)

    def load_data(self) -> pd.DataFrame:
        """Load data from the configured source."""
        return self.data_source.read_data()

    def get_filtered_data(self, column: str, value: str) -> pd.DataFrame:
        """Get data filtered by column and value."""
        df = self.load_data()
        # Case-insensitive matching
        if column == 'country_name':
            return df[df[column].str.upper() == value.upper()].copy()
        return df[df[column] == value].copy()

    def update_records(self, updated_df: pd.DataFrame) -> bool:
        """Update records in the data source."""
        try:
            # Load current data
            current_df = self.load_data()
            
            # Remove rows that were updated
            mask = ~current_df['id'].isin(updated_df['id'])
            filtered_df = current_df[mask]
            
            # Append updated rows
            final_df = pd.concat([filtered_df, updated_df], ignore_index=True)
            
            # Sort by ID
            final_df = final_df.sort_values('id')
            
            # Save back to source
            return self.data_source.write_data(final_df)
            
        except Exception as e:
            print(f"Error updating records: {str(e)}")
            return False