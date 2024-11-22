import pandas as pd
import random
import string
from config import DATA_PATH, TOKEN_FILE, FILTER_COLUMN

def generate_token(length=10):
    """Generate a random alphanumeric token."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def main():
    """Main function to generate tokens."""
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    unique_values = df[FILTER_COLUMN].dropna().unique()
    tokens = [{"country": value, "token": generate_token()} for value in unique_values]
    tokens.append({"country": "admin", "token": generate_token()})
    tokens_df = pd.DataFrame(tokens)
    tokens_df.to_csv(TOKEN_FILE, index=False)
    print(f"Tokens generated and saved to {TOKEN_FILE}")

if __name__ == "__main__":
    main()