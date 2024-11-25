"""Tests for admin functionality"""
import pytest
import json
from pathlib import Path
from crowdsourcing.admin.dashboard import save_config

def test_save_config(temp_config_file, sample_config):
    """Test saving configuration"""
    # Save configuration
    save_config(sample_config, temp_config_file)
    
    # Verify saved configuration
    with open(temp_config_file, 'r') as f:
        loaded_config = json.load(f)
    
    assert loaded_config == sample_config

def test_save_config_bad_path(sample_config):
    """Test saving configuration to invalid path raises exception"""
    with pytest.raises(Exception):
        save_config(sample_config, "/invalid/path/config.json")