# Museum Data Management System

A Streamlit-based application for managing museum data with token-based access control and support for both Dataiku DSS and CSV data sources.

## Features

- Token-based authentication
- Country-specific data access and management
- Admin dashboard with advanced features
- Support for both Dataiku DSS and CSV data sources
- Dynamic data editing capabilities
- Token management system

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- streamlit==1.40.2
- altair>=5.2.0
- pandas>=2.0.0
- openpyxl>=3.1.0
- xlsxwriter>=3.1.0

2. Configure your environment:
   - Create a `data` directory for CSV files (if using CSV mode)
   - Set up Dataiku DSS datasets (if using DSS mode)

## Configuration

The application uses `config.json` for configuration:

```json
{
    "APP_TITLE": "Museum Data Management",
    "APP_ICON": "🏛️",
    "HELP_TEXT": "Welcome to the Museum Data Management System",
    "DATA_SOURCE": {
        "type": "dss",  // or "csv"
        "settings": {
            "input_dataset": "MUSEUMS_INPUT",
            "output_dataset": "MUSEUMS_OUTPUT",
            "csv_path": "data/museums.csv"
        }
    },
    "TOKEN_FILE": "data/tokens.csv",
    "ADMIN_TOKEN": {
        "token": "admin",
        "country": "admin"
    }
}
```

### Data Source Configuration

#### For Dataiku DSS:
1. Set `type` to "dss"
2. Configure input and output dataset names in settings

#### For CSV:
1. Set `type` to "csv"
2. Ensure the csv_path points to your data file

## Running the Application

### Standard Mode:
```bash
streamlit run app.py
```

### In Dataiku Code Studio:
1. Configure your DSS datasets
2. Run the application using Dataiku's interface

## User Roles

### Admin User
- Access using the admin token from config.json
- Full data management capabilities
- Token management for countries
- Configuration management
- Dataset upload/management

### Country Users
- Access using country-specific tokens
- View and edit only their country's data
- Cannot access admin features
- Tokens managed by admin

## Directory Structure

```
streamlit-crowdsourcing/
├── app.py              # Main application
├── dashboard.py        # Admin dashboard
├── data_manager.py     # Data management
├── data_source.py      # Data source handler
├── config.py          # Configuration utilities
├── config.json        # Application configuration
├── requirements.txt   # Dependencies
├── data/              # Data directory (for CSV mode)
│   ├── museums.csv
│   └── tokens.csv
└── static/            # Static assets
    └── css/
        └── style.css
```

## Security Notes

- Keep your `config.json` secure as it contains the admin token
- Regularly rotate country tokens
- Back up your data regularly
- Monitor access logs if available

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Troubleshooting

Common issues and solutions:

1. Data source connection errors:
   - Check DSS dataset names
   - Verify CSV file paths
   - Ensure proper permissions

2. Token issues:
   - Verify token file exists
   - Check token file permissions
   - Confirm token format

3. Streamlit compatibility:
   - Ensure correct Streamlit version (1.40.2)
   - Check all dependencies are installed

## Support

For issues and questions:
1. Check the troubleshooting section
2. Submit an issue on GitHub
3. Contact the development team

## License

This project is licensed under MIT License - see the LICENSE file for details.
