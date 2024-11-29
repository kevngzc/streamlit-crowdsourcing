# Museum Data Crowdsourcing Application

A Streamlit application for museum data management through country-specific token access. The application supports both Dataiku DSS and local environments.

## Project Structure
```
streamlit-crowdsourcing/
├── app.py                 # Main application
├── config.py             # Configuration management
├── dashboard.py          # Admin dashboard interface
├── data_manager.py       # Data operations handler
├── data_source.py        # Data source interface
├── config.json           # Local configuration
├── requirements.txt      # Project dependencies
├── .streamlit/           # Streamlit configuration
└── data/                 # Data directory
    ├── museums.csv       # Museum database
    └── tokens.csv        # Access tokens
```

## Features

### Data Management
- Museum information tracking with fields:
  - Core: name, country, heritage status, description
  - Contact: operator, phone, email, address, website
  - Facilities: wheelchair access, entry fee, capacity
- Real-time data editing with validation
- Country-specific data access

### Security
- Token-based authentication
- SHA-256 based stable token generation
- Country-specific access control
- Admin dashboard for management

## Configuration

### Dataiku DSS Variables
```json
{
    "STREAMLIT_CROWDSOURCING": {
        "ADMIN_TOKEN": "your_secure_token",
        "DATA_PATH": "data/museums.csv",
        "TOKEN_FILE": "data/tokens.csv",
        "APP_TITLE": "Museum Data Crowdsourcing",
        "APP_ICON": "🏛️",
        "HELP_TEXT": "Welcome message",
        "FILTER_COLUMN": "country_name",
        "STREAMLIT_INPUT": "input_dataset_name",
        "STREAMLIT_OUTPUT": "output_dataset_name"
    }
}
```

### Local Development
Create config.json in project root:
```json
{
    "DATA_PATH": "data/museums.csv",
    "TOKEN_FILE": "data/tokens.csv",
    "APP_TITLE": "Museum Data Crowdsourcing",
    "APP_ICON": "🏛️",
    "HELP_TEXT": "Welcome message",
    "FILTER_COLUMN": "country_name",
    "ADMIN_TOKEN": "your_admin_token"
}
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd streamlit-crowdsourcing
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create data directory:
```bash
mkdir -p data
```

## Usage

### For Administrators
1. Access admin dashboard with admin token
2. Generate country access tokens
3. Download and distribute tokens
4. Monitor data submissions

### For Country Users
1. Log in with provided token
2. View/edit country museum data
3. Save changes as needed
4. Log out when finished

## Deployment

### In Dataiku DSS
1. Configure project variables
2. Set up webapp security:
```
PUBLIC_WEBAPPS_WHITELIST=your_webapp_id
your_webapp_id={"allow_public_access": true, "require_auth": false}
```

### Local Development
```bash
streamlit run app.py
```

## Dependencies
- Python 3.9+
- Streamlit 1.31.0+
- Pandas 2.0.0+
- Numpy 1.24.0+

## Security Features
- Stable token generation
- Data validation
- Type checking
- Case-insensitive matching
- Error handling
- Protected admin functions

## Contributing
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License
This project is licensed under the terms included in the LICENSE file.