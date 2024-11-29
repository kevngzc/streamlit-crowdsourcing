"""Main entry point for the crowdsourcing application."""
import json
import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional

from data_manager import DataManager
from config import load_config, save_config
from dashboard import render_admin_page

def render_home_page(config: Dict[str, Any]) -> Optional[str]:
    """Render the home page with token input."""
    st.markdown(
        f"""
        <div class="title-container">
            <div class="emoji">{config["APP_ICON"]}</div>
            <h1 class="title">{config["APP_TITLE"]}</h1>
            <p class="subtitle">Please enter your access token to continue</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.form(key="token_form"):
        input_token = st.text_input("Enter your token:", max_chars=10)
        submit_token = st.form_submit_button("Submit")
        return input_token if submit_token else None

def render_navigation():
    """Render navigation with home button."""
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("🏠 Home"):
            st.session_state.token = None
            st.rerun()

def load_tokens(token_file: str) -> Dict[str, str]:
    """Load and validate tokens."""
    try:
        Path(token_file).parent.mkdir(parents=True, exist_ok=True)
        if not Path(token_file).exists():
            # Create default token file
            tokens_df = pd.DataFrame({
                'token': ['admin'],
                'country': ['admin']
            })
            tokens_df.to_csv(token_file, index=False)
            return dict(zip(tokens_df["token"], tokens_df["country"]))
            
        tokens_df = pd.read_csv(token_file)
        return dict(zip(tokens_df["token"], tokens_df["country"]))
    except Exception as e:
        st.error(f"Error loading tokens: {str(e)}")
        return {'admin': 'admin'}  # Default admin token

def render_country_page(data_manager: DataManager, country: str, config: Dict[str, Any]):
    """Render the country-specific interface."""
    st.subheader(f"Museum Data for {country}")
    
    try:
        country_data = data_manager.get_filtered_data("country_name", country)
        
        if country_data.empty:
            st.warning(f"No museum data available for {country}")
            return
        
        edited_df = st.data_editor(
            country_data,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "country_name": st.column_config.TextColumn(
                    "Country",
                    help="Country name",
                    disabled=True
                ),
                "name": st.column_config.TextColumn(
                    "Name",
                    help="Museum name",
                    required=True
                ),
                "heritage": st.column_config.CheckboxColumn(
                    "Heritage Site",
                    help="Check if this is a heritage site"
                ),
                "description": st.column_config.TextColumn(
                    "Description",
                    help="Description",
                    max_chars=500
                ),
                "website": st.column_config.LinkColumn(
                    "Website",
                    help="Website URL"
                ),
                "id": st.column_config.NumberColumn(
                    "ID",
                    help="Unique identifier",
                    disabled=True
                )
            },
            hide_index=True
        )
        
        if st.button("Save Changes"):
            if data_manager.update_records(edited_df):
                st.success("Changes saved successfully!")
            else:
                st.error("Error saving changes")
                
    except Exception as e:
        st.error(f"Error displaying data: {str(e)}")

def load_css():
    """Load custom CSS styles."""
    try:
        css_path = Path("static/css/style.css")
        if css_path.exists():
            with open(css_path, "r") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning("Custom styling could not be loaded.")

def main():
    """Main application entry point."""
    try:
        # Load configuration
        config = load_config()
        
        # Configure Streamlit page
        st.set_page_config(
            page_title=config["APP_TITLE"],
            page_icon=config["APP_ICON"],
            layout="wide"
        )
        
        # Load custom CSS
        load_css()
        
        # Initialize session state
        if "token" not in st.session_state:
            st.session_state.token = None
        
        # Render navigation
        render_navigation()
        
        # Load tokens and initialize data manager
        tokens = load_tokens(config["TOKEN_FILE"])
        data_manager = DataManager(config)
        
        # Sidebar
        st.sidebar.title("Navigation")
        st.sidebar.markdown(config["HELP_TEXT"])
        
        # Main content
        if not st.session_state.token:
            input_token = render_home_page(config)
            if input_token:
                if input_token in tokens:
                    st.session_state.token = input_token
                    st.rerun()
                else:
                    st.error("Invalid token. Please try again.")
        else:
            # Get user's country or admin status
            country = tokens.get(st.session_state.token)
            
            if country == "admin":
                render_admin_page(config, data_manager.load_data())
            else:
                render_country_page(data_manager, country, config)
            
            # Logout button
            if st.sidebar.button("Logout"):
                st.session_state.token = None
                st.rerun()
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.error("Please check your configuration and data files.")

if __name__ == "__main__":
    main()