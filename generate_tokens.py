import pandas as pd
import random
import string
import json
from pathlib import Path

def load_config():
    """Load configuration from config.json"""
    with open("config.json", "r") as f:
        return json.load(f)

def generate_token(length=10):
    """Generate a random alphanumeric token."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def main():
    """Main function to generate tokens."""
    # Load configuration
    config = load_config()
    
    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)
    
    try:
        # Read the museum data CSV with more flexible parsing
        df = pd.read_csv(
            config["DATA_PATH"],
            encoding="utf-8",
            on_bad_lines='skip',  # Skip problematic lines
            skipinitialspace=True,  # Skip initial spaces
            engine='python'  # Use python engine for more flexible parsing
        )
        
        # Clean up the country column name if it has an asterisk
        country_col = config["FILTER_COLUMN"]
        if country_col.startswith('*'):
            country_col = country_col.lstrip('*')
            
        # Get unique country values and clean them
        unique_countries = df[country_col].dropna().unique()
        # Clean up country codes (remove spaces and convert to uppercase)
        unique_countries = [str(c).strip().upper() for c in unique_countries if str(c).strip()]
        
        # Generate tokens for each country
        tokens = [
            {"country": country, "token": generate_token()} 
            for country in unique_countries
        ]
        
        # Add admin token
        tokens.append({"country": "admin", "token": generate_token()})
        
        # Create DataFrame and save to CSV
        tokens_df = pd.DataFrame(tokens)
        tokens_df.to_csv(config["TOKEN_FILE"], index=False)
        
        print(f"Successfully generated {len(tokens)} tokens")
        print(f"Tokens saved to {config['TOKEN_FILE']}")
        print("\nToken list:")
        for token in tokens:
            print(f"{token['country']}: {token['token']}")
            
    except Exception as e:
        print(f"Error generating tokens: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()