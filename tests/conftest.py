"""Test fixtures and configuration."""
import pytest
import pandas as pd
import tempfile
import json
from pathlib import Path

@pytest.fixture
def sample_config():
    """Fixture providing sample configuration"""
    return {
        "DATA_PATH": "data/data.csv",
        "TOKEN_FILE": "data/tokens.csv",
        "APP_TITLE": "Data Crowdsourcing Platform",
        "APP_ICON": "📊",
        "FILTER_COLUMN": "country_name",
        "HELP_TEXT": "Welcome to the Data Crowdsourcing platform!"
    }

@pytest.fixture
def sample_museums_df():
    """Fixture providing sample museum data"""
    return pd.DataFrame({
        'country_name': ['Malawi', 'Malawi'],
        'name': ['Museum 1', 'Museum 2'],
        'heritage': [True, False],
        'description': ['Desc 1', 'Desc 2'],
        'website': ['http://museum1.com', 'http://museum2.com'],
        'id': [1, 2]
    })

@pytest.fixture
def temp_csv_file():
    """Fixture providing a temporary CSV file"""
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w', delete=False) as f:
        yield Path(f.name)
        try:
            Path(f.name).unlink()  # Cleanup after test
        except FileNotFoundError:
            pass  # File was already deleted

@pytest.fixture
def temp_config_file():
    """Fixture providing a temporary config file"""
    with tempfile.NamedTemporaryFile(suffix='.json', mode='w', delete=False) as f:
        yield Path(f.name)
        try:
            Path(f.name).unlink()  # Cleanup after test
        except FileNotFoundError:
            pass  # File was already deleted