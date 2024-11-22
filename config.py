# config.py

# Path to the dataset
DATA_PATH = 'data/museum_osm_raw_data.csv'

# Path to store the generated tokens
TOKEN_FILE = 'data/tokens.csv'

# Column used to generate tokens for filtering
FILTER_COLUMN = 'country_name'

# General app settings
APP_TITLE = "Data Update Portal"
APP_ICON = "🌍"
HELP_TEXT = """
### How to use the app:
1. Enter your token on the home page.
2. If valid, view the filtered data for your country.
3. Edit values directly in the table.
4. Save your changes when done!
"""