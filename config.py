"""Configuration management module."""
import json
import streamlit as st
from pathlib import Path
from typing import Dict, Any

def is_dataiku_environment():
    """Check if running in Dataiku environment"""
    try:
        import dataiku
        return True
    except ImportError:
        return False

def load_config() -> Dict[str, Any]:
    """Load configuration from either Dataiku project variables or config.json"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    config_path = Path("config.json")
    
    default_config = {
        "DATA_PATH": str(data_dir / "museums.csv"),
        "TOKEN_FILE": str(data_dir / "tokens.csv"),
        "APP_TITLE": "Museum Data Crowdsourcing",
        "APP_ICON": "🏛️",
        "HELP_TEXT": """
        Welcome to the Museum Data Crowdsourcing platform!
        
        Use your provided token to access and update museum information
        for your country. Changes are saved automatically.
        
        For support, please contact the administrator.
        """,
        "FILTER_COLUMN": "country_name",
        "ADMIN_TOKEN": None,
        "AUTH": {
            "enable_auth": True,
            "session_expiry": 3600
        }
    }
    
    try:
        if is_dataiku_environment():
            # Load from Dataiku project variables
            import dataiku
            variables = dataiku.get_custom_variables()
            
            if not variables:
                raise ValueError("No project variables found")
            
            # Get Streamlit configuration from project variables
            streamlit_config = variables.get('STREAMLIT_CROWDSOURCING')
            
            if not streamlit_config:
                raise ValueError("STREAMLIT_CROWDSOURCING configuration not found in project variables")
            
            # If streamlit_config is a string, try to parse it as JSON
            if isinstance(streamlit_config, str):
                try:
                    streamlit_config = json.loads(streamlit_config)
                except json.JSONDecodeError:
                    raise ValueError("STREAMLIT_CROWDSOURCING configuration is not valid JSON")
            
            # Merge with default config
            config = {**default_config, **streamlit_config}
            
        else:
            # Load from config.json
            if not config_path.exists():
                # Save default configuration
                with open(config_path, "w") as f:
                    json.dump(default_config, f, indent=4)
                return default_config
            
            with open(config_path, "r") as f:
                file_config = json.load(f)
                # Merge with default config
                config = {**default_config, **file_config}
        
        # Validate required configuration
        if not config.get('ADMIN_TOKEN'):
            raise ValueError("ADMIN_TOKEN not found in configuration")
            
        # Ensure all paths are relative to the data directory
        config['DATA_PATH'] = str(data_dir / Path(config['DATA_PATH']).name)
        config['TOKEN_FILE'] = str(data_dir / Path(config['TOKEN_FILE']).name)
        
        return config
        
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")
        return default_config

def save_config(config: Dict[str, Any], config_path: str = "config.json") -> None:
    """Save configuration to config.json"""
    if is_dataiku_environment():
        st.warning("Configuration cannot be saved when running in Dataiku environment")
        return
        
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        st.error(f"Error saving configuration: {str(e)}")
        raise