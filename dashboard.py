"""Admin dashboard functionality."""
import streamlit as st
import pandas as pd
import hashlib
from pathlib import Path
from typing import Dict, Any

def generate_stable_token(country: str) -> str:
    """Generate a stable 10-character token based on country name."""
    # Ensure country is a string and not NaN or empty
    if pd.isna(country) or not str(country).strip():
        return ""
    
    country_str = str(country).strip().upper()
    # Create a hash of the country name
    hash_object = hashlib.sha256(country_str.encode())
    hash_hex = hash_object.hexdigest()
    # Take first 10 characters and convert to uppercase
    return hash_hex[:10].upper()

def handle_dataset_management(config: Dict[str, Any], current_df: pd.DataFrame) -> None:
    """Handle dataset viewing and management"""
    st.markdown("### Dataset Management")
    
    # Display current dataset
    if not current_df.empty:
        st.dataframe(
            current_df,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.warning("No data available in the dataset")

def handle_token_management(config: Dict[str, Any], df: pd.DataFrame) -> None:
    """Handle token viewing and management"""
    st.markdown("### Token Management")

    if st.button("Generate Tokens for All Countries"):
        try:
            if df.empty or 'country_name' not in df.columns:
                st.error("No valid data available to generate tokens")
                return
            
            # Convert country_name to string and clean data
            cleaned_countries = df['country_name'].apply(lambda x: str(x).strip() if not pd.isna(x) else "")
            unique_countries = sorted([c for c in cleaned_countries.unique() if c])  # Filter out empty strings
            
            tokens = []
            for country in unique_countries:
                token = generate_stable_token(country)
                if token:  # Only add if we got a valid token
                    tokens.append({
                        'country': country,
                        'token': token
                    })
            
            # Create tokens DataFrame
            if tokens:  # Only proceed if we have valid tokens
                tokens_df = pd.DataFrame(tokens)
                tokens_df = tokens_df.sort_values('country').reset_index(drop=True)
                
                # Add admin token if configured
                admin_token = config.get('ADMIN_TOKEN')
                if admin_token:
                    admin_row = pd.DataFrame([{
                        'country': 'admin',
                        'token': admin_token
                    }])
                    tokens_df = pd.concat([admin_row, tokens_df], ignore_index=True)
                
                # Save tokens
                token_file = config["TOKEN_FILE"]
                Path(token_file).parent.mkdir(parents=True, exist_ok=True)
                tokens_df.to_csv(token_file, index=False)
                
                st.success(f"Generated tokens for {len(tokens)} countries")
                
                # Display the tokens
                st.dataframe(
                    tokens_df,
                    column_config={
                        "country": st.column_config.TextColumn("Country"),
                        "token": st.column_config.TextColumn("Token")
                    },
                    hide_index=True
                )
                
                # Add download button
                st.download_button(
                    "Download Tokens CSV",
                    tokens_df.to_csv(index=False).encode('utf-8'),
                    "tokens.csv",
                    "text/csv"
                )
            else:
                st.warning("No valid countries found to generate tokens")
                
        except Exception as e:
            st.error(f"Error generating tokens: {str(e)}")
            st.error("Debug info:")
            st.write("DataFrame info:", df.info())
            st.write("Country name types:", df['country_name'].apply(type).unique())
    
    # Display current tokens if they exist
    try:
        token_file = config["TOKEN_FILE"]
        if Path(token_file).exists():
            tokens_df = pd.read_csv(token_file)
            st.markdown("### Current Tokens")
            st.dataframe(
                tokens_df,
                column_config={
                    "country": st.column_config.TextColumn("Country"),
                    "token": st.column_config.TextColumn("Token")
                },
                hide_index=True
            )
            
            # Add download button for current tokens
            st.download_button(
                "Download Current Tokens",
                tokens_df.to_csv(index=False).encode('utf-8'),
                "current_tokens.csv",
                "text/csv"
            )
    except Exception as e:
        st.error(f"Error loading current tokens: {str(e)}")

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
        handle_dataset_management(config, df)
        
    with tokens_tab:
        handle_token_management(config, df)
        
    with config_tab:
        handle_configuration(config)