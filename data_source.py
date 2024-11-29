"""Data source handler for both DSS and CSV data."""
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import os
from pathlib import Path
import uuid

class DataSourceManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.is_dss = self._check_dss_environment()
        
    def _check_dss_environment(self) -> bool:
        """Check if running in Dataiku environment."""
        try:
            import dataiku
            return True
        except ImportError:
            return False

    def read_data(self) -> pd.DataFrame:
        """Read data from configured source."""
        if self.is_dss and self.config.get("STREAMLIT_INPUT"):
            df = self._read_dss_data()
        else:
            df = self._read_csv_data()
            
        # Convert country_name to title case and handle data types
        if not df.empty:
            if 'country_name' in df.columns:
                df['country_name'] = df['country_name'].str.title()
            if 'capacity' in df.columns:
                df['capacity'] = pd.to_numeric(df['capacity'], errors='coerce').fillna(0).astype(int)
            if 'fee' in df.columns:
                df['fee'] = pd.to_numeric(df['fee'], errors='coerce').fillna(0.0)
            
        return df

    def generate_tokens(self) -> bool:
        """Generate tokens for countries in the dataset."""
        try:
            # Read current data
            df = self.read_data()
            token_file = self.config["TOKEN_FILE"]
            Path(token_file).parent.mkdir(parents=True, exist_ok=True)
            
            # Get unique countries from the dataset
            if not df.empty:
                unique_countries = df['country_name'].unique()
            else:
                return False
                
            # Initialize or load existing tokens DataFrame
            if os.path.exists(token_file):
                tokens_df = pd.read_csv(token_file)
            else:
                tokens_df = pd.DataFrame(columns=['country', 'token'])
            
            # Generate new tokens for countries that don't have them
            existing_countries = set(tokens_df['country'].str.upper())
            new_tokens = []
            
            for country in unique_countries:
                if pd.notna(country) and country.upper() not in existing_countries:
                    token = str(uuid.uuid4())[:8].upper()
                    new_tokens.append({
                        'country': country,
                        'token': token
                    })
            
            if new_tokens:
                # Add new tokens to existing ones
                new_tokens_df = pd.DataFrame(new_tokens)
                tokens_df = pd.concat([tokens_df, new_tokens_df], ignore_index=True)
                
                # Remove duplicates and save
                tokens_df = tokens_df.drop_duplicates(subset=['country'], keep='first')
                tokens_df.to_csv(token_file, index=False)
                print(f"Generated tokens for {len(new_tokens)} new countries")
            
            return True
            
        except Exception as e:
            print(f"Error generating tokens: {str(e)}")
            return False

    def _read_dss_data(self) -> pd.DataFrame:
        """Read data from DSS dataset."""
        try:
            import dataiku
            dataset = dataiku.Dataset(self.config["STREAMLIT_INPUT"])
            return dataset.get_dataframe()
        except Exception as e:
            print(f"Error reading DSS data: {str(e)}")
            return pd.DataFrame()

    def _write_dss_data(self, df: pd.DataFrame) -> bool:
        """Write data to DSS dataset."""
        try:
            import dataiku
            dataset = dataiku.Dataset(self.config["STREAMLIT_OUTPUT"])
            dataset.write_with_schema(df)
            return True
        except Exception as e:
            print(f"Error writing DSS data: {str(e)}")
            return False

    def _read_csv_data(self) -> pd.DataFrame:
        """Read data from CSV file."""
        try:
            csv_path = self.config["DATA_PATH"]
            if os.path.exists(csv_path):
                return pd.read_csv(csv_path)
            print(f"CSV file not found at {csv_path}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error reading CSV data: {str(e)}")
            return pd.DataFrame()

    def _write_csv_data(self, df: pd.DataFrame) -> bool:
        """Write data to CSV file."""
        try:
            csv_path = self.config["DATA_PATH"]
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            df.to_csv(csv_path, index=False)
            return True
        except Exception as e:
            print(f"Error writing CSV data: {str(e)}")
            return False