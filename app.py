import streamlit as st
import pandas as pd
from config import DATA_PATH, TOKEN_FILE, APP_TITLE, APP_ICON, HELP_TEXT

# Configure the app layout
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

# Load tokens
tokens_df = pd.read_csv(TOKEN_FILE)
tokens = dict(zip(tokens_df["token"], tokens_df["country"]))

# Load dataset
try:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
except Exception as e:
    st.error(f"Error loading data: {e}")
    df = pd.DataFrame()

# Initialize token in session state
if "token" not in st.session_state:
    st.session_state.token = None

# Home Page: Prompt for token if none is set
if not st.session_state.token:
    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f7fa;
        }
        .title-container {
            text-align: center;
            padding: 2rem 0;
        }
        .title {
            font-size: 3rem;
            font-weight: bold;
            color: #2c3e50;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #7f8c8d;
            margin-bottom: 2rem;
        }
        .emoji {
            font-size: 5rem;
            margin-bottom: 1rem;
        }
        .form-container {
            margin: auto;
            width: 50%;
            text-align: center;
        }
        .stButton>button {
            background-color: #3498db;
            color: white;
            font-size: 1rem;
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover {
            background-color: #2980b9;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <div class="title-container">
            <div class="emoji">🌍</div>
            <h1 class="title">Welcome to the Data Update Portal</h1>
            <p class="subtitle">Use this portal to view and edit museum data for your assigned country.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form(key="token_form"):
        input_token = st.text_input("Enter your token (10 characters):", max_chars=10)
        submit_token = st.form_submit_button("Submit")
        if submit_token:
            if input_token in tokens:
                st.session_state.token = input_token  # Save the token to session state
                st.rerun()  # Refresh the app
            else:
                st.error("Invalid token. Please try again.")
    st.stop()

# Determine the country or admin access based on the token
token = st.session_state.token
selected_country = tokens[token]

# Sidebar for navigation and help
st.sidebar.title("Navigation")
st.sidebar.info(HELP_TEXT)

# Header
st.title(APP_TITLE)
if selected_country == "admin":
    st.subheader("Admin Access: All Countries")
    filtered_df = df
else:
    st.subheader(f"Country: {selected_country.capitalize()}")
    filtered_df = df[df["country_name"].str.strip().str.lower() == selected_country.strip().lower()]

# Display filtered data
if filtered_df.empty:
    st.warning("No data available.")
else:
    st.write("### Review and Modify Data Below")
    edited_df = st.data_editor(filtered_df, num_rows="dynamic", use_container_width=True)

    # Save Changes
    if st.button("Save Changes"):
        try:
            for index, row in edited_df.iterrows():
                df.loc[df["osm_id"] == row["osm_id"], :] = row
            df.to_csv(DATA_PATH, index=False)
            st.success("Your changes have been saved successfully!")
        except Exception as e:
            st.error(f"An error occurred while saving changes: {e}")
