"""Tests for data management functionality"""
import pytest
import pandas as pd
from pathlib import Path
from crowdsourcing.core.data_manager import DataManager

@pytest.fixture
def data_manager(sample_config, temp_csv_file):
    """Fixture providing a DataManager instance with temp file"""
    config = sample_config.copy()
    config["DATA_PATH"] = str(temp_csv_file)
    return DataManager(config)

def test_load_data(data_manager, temp_csv_file, sample_museums_df):
    """Test loading data from CSV"""
    # Setup: Save sample data to temporary file
    sample_museums_df.to_csv(temp_csv_file, index=False)
    
    # Test loading data
    loaded_df = data_manager.load_data()
    
    # Verify data was loaded correctly
    assert not loaded_df.empty
    assert len(loaded_df) == len(sample_museums_df)
    assert all(col in loaded_df.columns for col in sample_museums_df.columns)

def test_load_data_with_invalid_file(sample_config):
    """Test loading data from non-existent file"""
    config = sample_config.copy()
    config["DATA_PATH"] = "nonexistent_file.csv"
    manager = DataManager(config)
    df = manager.load_data()
    assert df.empty

def test_save_data(data_manager, sample_museums_df):
    """Test saving data to CSV"""
    # Test saving data
    success = data_manager.save_data(sample_museums_df)
    assert success
    
    # Verify saved data
    saved_df = pd.read_csv(data_manager.data_path)
    pd.testing.assert_frame_equal(
        saved_df.sort_index(axis=1),
        sample_museums_df.sort_index(axis=1)
    )

def test_save_data_with_invalid_path(sample_config, sample_museums_df):
    """Test saving data to invalid path"""
    config = sample_config.copy()
    config["DATA_PATH"] = "/invalid/path/file.csv"
    manager = DataManager(config)
    success = manager.save_data(sample_museums_df)
    assert not success