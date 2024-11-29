"""Configuration management module."""
import json
import streamlit as st
from pathlib import Path
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    config_path = data_dir / "config.json"
    
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
        "FILTER_COLUMN": "country_name"
    }
    
    if not config_path.exists():
        # Save default configuration
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config
    
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")
        return default_config

def save_config(config: Dict[str, Any], config_path: str = "data/config.json") -> None:
    """Save configuration to config.json"""
    try:
        Path(config_path).parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        st.error(f"Error saving configuration: {str(e)}")
        raise