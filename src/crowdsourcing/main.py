import json
from pathlib import Path

# Import admin module
import admin  # This imports the new admin.py module
import pandas as pd
import streamlit as st


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
            "FILTER_COLUMN": "country_name",
        }

    with open(config_path, "r") as f:
        return json.load(f)


# [Previous data management functions remain the same]
def load_data(file_path):
    """Load and validate museum data"""
    try:
        df = pd.read_csv(
            file_path, encoding="utf-8", engine="python", on_bad_lines="skip"
        )

        df.columns = [col.strip() for col in df.columns]

        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("").astype(str).str.strip()

        df["heritage"] = df["heritage"].map({"True": True, "False": False})
        df["website"] = df["website"].str.replace(r"[,*]+", "", regex=True).str.strip()

        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
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
        return dict(zip(tokens_df["token"], tokens_df["country"]))
    except Exception as e:
        st.error(f"Error loading tokens: {str(e)}")
        return {}


# [Previous UI Components remain the same]
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
        unsafe_allow_html=True,
    )

    with st.form(key="token_form"):
        input_token = st.text_input("Enter your token:", max_chars=10)
        submit_token = st.form_submit_button("Submit")
        return input_token if submit_token else None


def render_country_page(df, country, config):
    """Render the country-specific interface"""
    st.subheader(f"Museum Data for {country}")

    try:
        country_data = df[df["country_name"].str.lower() == country.lower()].copy()

        if country_data.empty:
            st.warning(f"No museum data available for {country}")
            return

        edited_df = st.data_editor(
            country_data,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "country_name": st.column_config.TextColumn(
                    "Country", help="Country name", disabled=True
                ),
                "name": st.column_config.TextColumn(
                    "Name", help="Museum name", required=True
                ),
                "address": st.column_config.TextColumn(
                    "Address", help="Museum address"
                ),
                "heritage": st.column_config.CheckboxColumn(
                    "Heritage Site", help="Check if this is a heritage site"
                ),
                "description": st.column_config.TextColumn(
                    "Description", help="Museum description", max_chars=500
                ),
                "website": st.column_config.LinkColumn(
                    "Website", help="Museum website URL"
                ),
                "id": st.column_config.NumberColumn(
                    "ID", help="Museum ID", disabled=True
                ),
            },
            hide_index=True,
        )

        if st.button("Save Changes"):
            try:
                for index, row in edited_df.iterrows():
                    df.loc[df["id"] == row["id"]] = row

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
        page_title=config["APP_TITLE"], page_icon=config["APP_ICON"], layout="wide"
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
            # Use the admin module instead of the previous admin code
            admin.render_admin_page(config, df)
        else:
            render_country_page(df, country, config)

        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state.token = None
            st.query_params.clear()
            st.rerun()


if __name__ == "__main__":
    main()
