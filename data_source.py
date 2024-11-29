"""Data source handler for both DSS and CSV data."""
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import os
from pathlib import Path
import uuid
import streamlit as st

class DataSourceManager:
    @classmethod
    def create(cls, config: Dict[str, Any]):
        """Factory method to create DataSourceManager instance"""
        instance = cls()
        instance.config = config
        instance.is_dss = instance._check_dss_environment()
        return instance
        
    def __init__(self):
        """Initialize without arguments"""
        self.config = {}
        self.is_dss = False
        
    def _check_dss_environment(self) -> bool:
        """Check if running in Dataiku environment."""
        try:
            import dataiku
            return True
        except ImportError:
            return False

    def read_data(self) -> pd.DataFrame:
        """Read data from configured source."""
        try:
            if self.is_dss and self.config.get("STREAMLIT_INPUT"):
                print("Reading from DSS dataset:", self.config.get("STREAMLIT_INPUT"))
                df = self._read_dss_data()
            else:
                print("Reading from CSV file:", self.config.get("DATA_PATH"))
                df = self._read_csv_data()
                
            # Convert country_name to title case and handle data types
            if not df.empty:
                if 'country_name' in df.columns:
                    df['country_name'] = df['country_name'].str.title()
                if 'capacity' in df.columns:
                    df['capacity'] = pd.to_numeric(df['capacity'], errors='coerce').fillna(0).astype(int)
                if 'fee' in df.columns:
                    df['fee'] = pd.to_numeric(df['fee'], errors='coerce').fillna(0.0)
                if 'heritage' in df.columns:
                    df['heritage'] = df['heritage'].astype(bool)
                if 'wheelchair' in df.columns:
                    df['wheelchair'] = df['wheelchair'].astype(bool)
                if 'id' in df.columns:
                    df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype(int)
                
            print("Data loaded successfully, shape:", df.shape)
            return df
            
        except Exception as e:
            print(f"Error reading data: {str(e)}")
            st.error(f"Error reading data: {str(e)}")
            return pd.DataFrame()

    def write_data(self, df: pd.DataFrame) -> bool:
        """Write data to configured destination."""
        try:
            print("Writing data with shape:", df.shape)
            
            # Validate data types before writing
            if 'capacity' in df.columns:
                df['capacity'] = pd.to_numeric(df['capacity'], errors='coerce').fillna(0).astype(int)
            if 'fee' in df.columns:
                df['fee'] = pd.to_numeric(df['fee'], errors='coerce').fillna(0.0)
            if 'heritage' in df.columns:
                df['heritage'] = df['heritage'].astype(bool)
            if 'wheelchair' in df.columns:
                df['wheelchair'] = df['wheelchair'].astype(bool)
            if 'id' in df.columns:
                df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype(int)
            
            if self.is_dss and self.config.get("STREAMLIT_OUTPUT"):
                return self._write_dss_data(df)
            else:
                return self._write_csv_data(df)
                
        except Exception as e:
            print(f"Error writing data: {str(e)}")
            st.error(f"Error writing data: {str(e)}")
            return False

    def _read_dss_data(self) -> pd.DataFrame:
        """Read data from DSS dataset."""
        try:
            import dataiku
            dataset = dataiku.Dataset(self.config["STREAMLIT_INPUT"])
            df = dataset.get_dataframe()
            print(f"Read DSS data successfully, shape: {df.shape}")
            return df
        except Exception as e:
            print(f"Error reading DSS data: {str(e)}")
            st.error(f"Error reading DSS data: {str(e)}")
            return pd.DataFrame()

    def _write_dss_data(self, df: pd.DataFrame) -> bool:
        """Write data to DSS dataset."""
        try:
            import dataiku
            dataset = dataiku.Dataset(self.config["STREAMLIT_OUTPUT"])
            dataset.write_with_schema(df)
            print(f"Wrote data to DSS successfully, shape: {df.shape}")
            return True
        except Exception as e:
            print(f"Error writing DSS data: {str(e)}")
            st.error(f"Error writing DSS data: {str(e)}")
            return False

    def _read_csv_data(self) -> pd.DataFrame:
        """Read data from CSV file."""
        try:
            csv_path = self.config["DATA_PATH"]
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                print(f"Read CSV data successfully, shape: {df.shape}")
                return df
            print(f"CSV file not found at {csv_path}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error reading CSV data: {str(e)}")
            st.error(f"Error reading CSV data: {str(e)}")
            return pd.DataFrame()

    def _write_csv_data(self, df: pd.DataFrame) -> bool:
        """Write data to CSV file."""
        try:
            csv_path = self.config["DATA_PATH"]
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            df.to_csv(csv_path, index=False)
            print(f"Wrote data to CSV successfully, shape: {df.shape}")
            return True
        except Exception as e:
            print(f"Error writing CSV data: {str(e)}")
            st.error(f"Error writing CSV data: {str(e)}")
            return False