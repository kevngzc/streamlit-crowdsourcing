"""Data management functionality."""
import pandas as pd
from typing import Dict, Any
from data_source import DataSourceManager
import streamlit as st

class DataManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_source = DataSourceManager.create(config)

    def load_data(self) -> pd.DataFrame:
        """Load data from the configured source."""
        return self.data_source.read_data()

    def get_filtered_data(self, column: str, value: str) -> pd.DataFrame:
        """Get data filtered by column and value."""
        df = self.load_data()
        # Case-insensitive matching for country_name
        if column == 'country_name':
            return df[df[column].str.upper() == value.upper()].copy()
        return df[df[column] == value].copy()

    def update_records(self, updated_df: pd.DataFrame) -> bool:
        """Update records in the data source."""
        try:
            # Load current data
            current_df = self.load_data()
            
            if current_df.empty:
                st.error("No existing data found")
                return False
            
            # Ensure both dataframes have the same columns
            current_columns = set(current_df.columns)
            updated_columns = set(updated_df.columns)
            
            if current_columns != updated_columns:
                st.error(f"Column mismatch. Expected: {current_columns}, Got: {updated_columns}")
                return False
            
            # Remove rows that were updated
            if 'id' not in current_df.columns or 'id' not in updated_df.columns:
                st.error("ID column missing")
                return False
                
            mask = ~current_df['id'].isin(updated_df['id'])
            filtered_df = current_df[mask]
            
            # Convert numeric columns to appropriate types
            numeric_columns = ['id', 'capacity']
            for col in numeric_columns:
                if col in updated_df.columns:
                    updated_df[col] = pd.to_numeric(updated_df[col], errors='coerce')
                    
            # Convert boolean columns
            boolean_columns = ['heritage', 'wheelchair']
            for col in boolean_columns:
                if col in updated_df.columns:
                    updated_df[col] = updated_df[col].astype(bool)
            
            # Append updated rows
            final_df = pd.concat([filtered_df, updated_df], ignore_index=True)
            
            # Sort by ID
            if 'id' in final_df.columns:
                final_df = final_df.sort_values('id')
            
            # Print debug info
            print("Updated DataFrame info:")
            print(final_df.info())
            print("\nSample of updated data:")
            print(final_df.head())
            
            # Save back to source
            success = self.data_source.write_data(final_df)
            if not success:
                st.error("Failed to write data to source")
                return False
                
            return True
            
        except Exception as e:
            st.error(f"Error updating records: {str(e)}")
            print(f"Detailed error: {str(e)}")  # For debugging
            return False