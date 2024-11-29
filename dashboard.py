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
            st.write("Preview of uploaded data:")
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

def handle_token_management(config: Dict[str, Any]) -> None:
    """Handle token viewing and management"""
    st.markdown("### Token Management")
    try:
        tokens_df = pd.read_csv(config["TOKEN_FILE"])
        st.dataframe(tokens_df)
        
        # Convert to Excel for download
        buffer = io.BytesIO()
        tokens_df.to_excel(buffer, engine='xlsxwriter', index=False)
        buffer.seek(0)
        
        st.download_button(
            label="Download Tokens as Excel",
            data=buffer,
            file_name="tokens.xlsx",
            mime="application/vnd.ms-excel"
        )
        
        # Add new token
        st.markdown("### Add New Token")
        with st.form("new_token"):
            new_country = st.text_input("Country/Region:")
            if st.form_submit_button("Generate Token"):
                import uuid
                new_token = str(uuid.uuid4())[:8]
                new_row = pd.DataFrame({
                    'token': [new_token],
                    'country': [new_country]
                })
                updated_tokens = pd.concat([tokens_df, new_row], ignore_index=True)
                updated_tokens.to_csv(config["TOKEN_FILE"], index=False)
                st.success(f"New token generated: {new_token}")
                st.rerun()
                
    except Exception as e:
        st.error(f"Error managing tokens: {str(e)}")

def handle_configuration(config: Dict[str, Any]) -> None:
    """Handle configuration management"""
    st.markdown("### Configuration")
    with st.form("config_form"):
        new_config = {
            "DATA_PATH": st.text_input("Data Path", value=config["DATA_PATH"]),
            "TOKEN_FILE": st.text_input("Token File", value=config["TOKEN_FILE"]),
            "APP_TITLE": st.text_input("App Title", value=config["APP_TITLE"]),
            "APP_ICON": st.text_input("App Icon", value=config["APP_ICON"]),
            "FILTER_COLUMN": st.text_input("Filter Column", value=config["FILTER_COLUMN"]),
            "HELP_TEXT": st.text_area("Help Text", value=config["HELP_TEXT"])
        }
        
        if st.form_submit_button("Save Configuration"):
            save_config(new_config)
            st.success("Configuration updated! Please refresh the page to see changes.")

def render_admin_page(config: Dict[str, Any], df: pd.DataFrame) -> None:
    """Main admin interface renderer"""
    st.subheader("Admin Dashboard")
    
    # Create tabs for better organization
    dataset_tab, tokens_tab, config_tab = st.tabs([
        "Dataset Management", 
        "Token Management",
        "Configuration"
    ])
    
    with dataset_tab:
        handle_dataset_upload(config, df)
        
    with tokens_tab:
        handle_token_management(config)
        
    with config_tab:
        handle_configuration(config)