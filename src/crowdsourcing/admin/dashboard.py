"""Admin dashboard functionality."""
import json
import streamlit as st
import pandas as pd
import io
from pathlib import Path
from typing import Dict, Any

def save_config(config: Dict[str, Any], config_path: str = "config.json") -> None:
    """Save configuration to config.json"""
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

def handle_dataset_upload(config: Dict[str, Any], current_df: pd.DataFrame) -> None:
    """Handle dataset upload and management"""
    st.markdown("### Dataset Management")
    uploaded_file = st.file_uploader("Upload new dataset", type=["csv"])
    
    if uploaded_file:
        try:
            new_data = pd.read_csv(uploaded_file)
            st.dataframe(new_data.head())
            
            action = st.radio(
                "Choose action:",
                ["Replace current dataset", "Append to current dataset"]
            )
            
            if st.button("Apply Changes"):
                if action == "Replace current dataset":
                    new_data.to_csv(config["DATA_PATH"], index=False)
                    st.success("Dataset replaced successfully!")
                else:
                    updated_data = pd.concat([current_df, new_data], ignore_index=True)
                    updated_data.to_csv(config["DATA_PATH"], index=False)
                    st.success("Data appended successfully!")
                    
        except Exception as e:
            st.error(f"Error processing uploaded file: {str(e)}")

def render_admin_page(config: Dict[str, Any], df: pd.DataFrame) -> None:
    """Main admin interface renderer"""
    st.subheader("Admin Dashboard")
    
    tabs = st.tabs(["Dataset", "Configuration"])
    
    with tabs[0]:
        handle_dataset_upload(config, df)