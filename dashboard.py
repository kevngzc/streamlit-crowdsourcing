"""Admin dashboard functionality."""
import streamlit as st
import pandas as pd
import uuid
from pathlib import Path
from typing import Dict, Any

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
                try:
                    if action == "Replace current dataset":
                        new_data.to_csv(config["DATA_PATH"], index=False)
                        st.success("Dataset replaced successfully!")
                    else:
                        updated_data = pd.concat([current_df, new_data], ignore_index=True)
                        updated_data.to_csv(config["DATA_PATH"], index=False)
                        st.success("Data appended successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving data: {str(e)}")
                    
        except Exception as e:
            st.error(f"Error processing uploaded file: {str(e)}")

def handle_token_management(config: Dict[str, Any]) -> None:
    """Handle token viewing and management"""
    st.markdown("### Token Management")
    try:
        token_file = config["TOKEN_FILE"]
        Path(token_file).parent.mkdir(parents=True, exist_ok=True)
        
        if Path(token_file).exists():
            tokens_df = pd.read_csv(token_file)
            st.dataframe(
                tokens_df,
                column_config={
                    "country": st.column_config.TextColumn("Country"),
                    "token": st.column_config.TextColumn("Token")
                },
                hide_index=True
            )
            
            if st.button("Download Tokens CSV"):
                st.download_button(
                    "Download Tokens",
                    tokens_df.to_csv(index=False).encode('utf-8'),
                    "tokens.csv",
                    "text/csv"
                )
        else:
            st.warning("No tokens file found.")
            
        # Add new token
        st.markdown("### Add New Token")
        with st.form("new_token"):
            new_country = st.text_input("Country/Region:")
            if st.form_submit_button("Generate Token"):
                new_token = str(uuid.uuid4())[:8].upper()
                new_row = pd.DataFrame({
                    'country': [new_country],
                    'token': [new_token]
                })
                
                if Path(token_file).exists():
                    tokens_df = pd.read_csv(token_file)
                    # Check if country already exists
                    if new_country.upper() in tokens_df['country'].str.upper().values:
                        st.error(f"Token already exists for {new_country}")
                        return
                    updated_tokens = pd.concat([tokens_df, new_row], ignore_index=True)
                else:
                    updated_tokens = new_row
                    
                updated_tokens.to_csv(token_file, index=False)
                st.success(f"New token generated for {new_country}: {new_token}")
                st.rerun()
                
    except Exception as e:
        st.error(f"Error managing tokens: {str(e)}")

def handle_configuration(config: Dict[str, Any]) -> None:
    """Handle configuration management"""
    st.markdown("### Configuration")
    
    # Check if in Dataiku environment
    try:
        import dataiku
        st.info("Configuration can only be modified through Dataiku project variables in DSS environment")
        st.json(config)
        return
    except ImportError:
        pass
    
    with st.form("config_form"):
        new_config = {
            "DATA_PATH": st.text_input("Data Path", value=config["DATA_PATH"]),
            "TOKEN_FILE": st.text_input("Token File", value=config["TOKEN_FILE"]),
            "APP_TITLE": st.text_input("App Title", value=config["APP_TITLE"]),
            "APP_ICON": st.text_input("App Icon", value=config["APP_ICON"]),
            "HELP_TEXT": st.text_area("Help Text", value=config["HELP_TEXT"]),
            "ADMIN_TOKEN": config.get("ADMIN_TOKEN")  # Preserve admin token
        }
        
        if st.form_submit_button("Save Configuration"):
            from config import save_config
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