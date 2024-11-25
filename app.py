import streamlit as st
import pandas as pd
import json
import io
from pathlib import Path

# Configuration management
def load_config():
    """Load configuration from config.json"""
    config_path = Path("config.json")
    if not config_path.exists():
        # Default configuration
        return {
            "DATA_PATH": "data/museums.csv",
            "TOKEN_FILE": "data/tokens.csv",
            "APP_TITLE": "Museum Data Crowdsourcing",
            "APP_ICON": "🏛️",
            "HELP_TEXT": """
            Welcome to the Museum Data Crowdsourcing platform!
            
            Use your provided token to access and update museum information
            for your country. Changes are saved automatically.
            
            For support, please contact the administrator.
            """,
            "FILTER_COLUMN": "country_name"
        }
    
    with open(config_path, "r") as f:
        return json.load(f)

def save_config(config):
    """Save configuration to config.json"""
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

# Data management functions
def load_data(file_path):
    """Load and validate museum data"""
    try:
        # Read CSV with more flexible parsing settings
        df = pd.read_csv(
            file_path,
            encoding="utf-8",
            engine='python',  # Use python engine for more flexible parsing
            on_bad_lines='skip'  # Skip problematic lines
        )
        
        # Clean up column names
        df.columns = [col.strip() for col in df.columns]
        
        # Clean up the data
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('').astype(str).str.strip()
        
        # Convert heritage column to boolean
        df['heritage'] = df['heritage'].map({'True': True, 'False': False})
        
        # Remove any empty website entries (if they're just commas or asterisks)
        df['website'] = df['website'].str.replace(r'[,*]+', '', regex=True).str.strip()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        import traceback
        st.error(f"Detailed error: {traceback.format_exc()}")
        return pd.DataFrame()

def save_data(df, file_path):
    """Save museum data with error handling"""
    try:
        df.to_csv(file_path, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False

def load_tokens(token_file):
    """Load and validate tokens"""
    try:
        tokens_df = pd.read_csv(token_file)
        # Create a mapping of token to country
        token_map = dict(zip(tokens_df["token"], tokens_df["country"]))
        return token_map
    except Exception as e:
        st.error(f"Error loading tokens: {str(e)}")
        return {}

# UI Components
def render_home_page(config):
    """Render the home page with token input"""
    st.markdown(
        f"""
        <div class="title-container">
            <div class="emoji">
                {config["APP_ICON"]}
            </div>
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

def render_admin_page(config, df):
    """Render the admin interface"""
    st.subheader("Admin Dashboard")
    
    # Dataset Management
    st.markdown("### Dataset Management")
    uploaded_file = st.file_uploader("Upload new dataset", type=["csv"])
    if uploaded_file:
        new_data = pd.read_csv(uploaded_file)
        st.dataframe(new_data.head())
        
        action = st.radio(
            "Choose action:",
            ["Replace current dataset", "Append to current dataset"]
        )
        
        if st.button("Apply Changes"):
            if action == "Replace current dataset":
                save_data(new_data, config["DATA_PATH"])
                st.success("Dataset replaced successfully!")
            else:
                updated_data = pd.concat([df, new_data], ignore_index=True)
                save_data(updated_data, config["DATA_PATH"])
                st.success("Data appended successfully!")
    
    # Token Management
    st.markdown("### Token Management")
    try:
        tokens_df = pd.read_csv(config["TOKEN_FILE"])
        st.dataframe(tokens_df)
        
        # Convert to Excel
        buffer = io.BytesIO()
        tokens_df.to_excel(buffer, engine='xlsxwriter', index=False)
        buffer.seek(0)
        
        st.download_button(
            label="Download Tokens as Excel",
            data=buffer,
            file_name="tokens.xlsx",
            mime="application/vnd.ms-excel"
        )
    except Exception as e:
        st.error(f"Error loading tokens: {str(e)}")
        import traceback
        st.error(f"Detailed error: {traceback.format_exc()}")
    
    # Configuration Management
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

def render_country_page(df, country, config):
    """Render the country-specific interface"""
    st.subheader(f"Museum Data for {country}")
    
    try:
        # Filter data for the specific country
        country_data = df[df['country_name'].str.lower() == country.lower()].copy()
        
        if country_data.empty:
            st.warning(f"No museum data available for {country}")
            return
        
        # Create editable dataframe with specific column configurations
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
                "address": st.column_config.TextColumn(
                    "Address",
                    help="Museum address"
                ),
                "heritage": st.column_config.CheckboxColumn(
                    "Heritage Site",
                    help="Check if this is a heritage site"
                ),
                "description": st.column_config.TextColumn(
                    "Description",
                    help="Museum description",
                    max_chars=500
                ),
                "website": st.column_config.LinkColumn(
                    "Website",
                    help="Museum website URL"
                ),
                "id": st.column_config.NumberColumn(
                    "ID",
                    help="Museum ID",
                    disabled=True
                )
            },
            hide_index=True
        )
        
        if st.button("Save Changes"):
            try:
                # Update the main dataframe with edited data
                for index, row in edited_df.iterrows():
                    df.loc[df['id'] == row['id']] = row
                
                # Save the updated dataframe
                save_data(df, config["DATA_PATH"])
                st.success("Changes saved successfully!")
            except Exception as e:
                st.error(f"Error saving changes: {str(e)}")
                
    except Exception as e:
        st.error(f"Error displaying data: {str(e)}")
        import traceback
        st.error(f"Detailed error: {traceback.format_exc()}")

def render_navigation():
    """Render navigation with home button"""
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("🏠 Home"):
            st.session_state.token = None
            st.query_params.clear()
            st.rerun()

def load_css():
    """Load custom CSS styles"""
    try:
        with open("style.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning("Custom styling could not be loaded.")

def main():
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
        st.session_state.token = st.query_params.get("token", None)
    
    # Render navigation
    render_navigation()
    
    # Load tokens and data
    tokens = load_tokens(config["TOKEN_FILE"])
    df = load_data(config["DATA_PATH"])
    
    # Sidebar
    st.sidebar.title("Navigation")
    st.sidebar.markdown(config["HELP_TEXT"])
    
    # Main content
    if not st.session_state.token:
        input_token = render_home_page(config)
        if input_token:
            if input_token in tokens:
                st.session_state.token = input_token
                st.query_params["token"] = input_token
                st.rerun()
            else:
                st.error("Invalid token. Please try again.")
    else:
        # Get user's country or admin status
        country = tokens.get(st.session_state.token)
        
        if country == "admin":
            render_admin_page(config, df)
        else:
            render_country_page(df, country, config)
        
        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state.token = None
            st.query_params.clear()
            st.rerun()

if __name__ == "__main__":
    main()