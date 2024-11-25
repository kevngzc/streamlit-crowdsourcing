"""Token generation script for the crowdsourcing platform."""
import pandas as pd
import uuid
from pathlib import Path

def generate_token():
    """Generate a unique token."""
    return str(uuid.uuid4())[:8]

def ensure_data_directory():
    """Ensure data directory exists."""
    Path("data").mkdir(exist_ok=True)

def create_default_tokens():
    """Create default token file if it doesn't exist."""
    ensure_data_directory()
    token_file = Path("data/tokens.csv")
    
    if not token_file.exists():
        # Create sample tokens
        tokens_data = {
            'token': [generate_token() for _ in range(3)],
            'country': ['Sample Country 1', 'Sample Country 2', 'admin']
        }
        df = pd.DataFrame(tokens_data)
        df.to_csv(token_file, index=False)
        print(f"Created default tokens file at {token_file}")
        print("\nDefault tokens:")
        print(df)
    else:
        print(f"Token file already exists at {token_file}")
        df = pd.read_csv(token_file)
        print("\nExisting tokens:")
        print(df)

def main():
    """Main function to generate tokens."""
    try:
        create_default_tokens()
    except Exception as e:
        print(f"Error generating tokens: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())