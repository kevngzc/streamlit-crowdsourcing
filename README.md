# CSV Crowdsourcing Platform

A Streamlit-based platform for collaborative data management with region-specific access control.

## Features

- Region-specific data access and editing
- Token-based authentication
- Admin dashboard with full management capabilities
- Real-time data editing
- Excel export for token management
- Flexible CSV data structure

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/csv-crowdsourcing.git
cd csv-crowdsourcing

# Install dependencies
poetry install

# Generate initial tokens
poetry run generate-tokens

# Start application
poetry run start
```

## Project Structure

```
csv-crowdsourcing/
├── src/                      # Source code
│   └── crowdsourcing/
│       ├── admin/           # Admin dashboard
│       ├── core/            # Core functionality
│       ├── ui/              # UI components
│       ├── main.py         # Main application
│       └── cli.py          # CLI interface
├── tests/                   # Unit tests
├── scripts/                 # Utility scripts
├── static/                  # Static assets
│   ├── css/                # Styling
│   └── templates/          # HTML templates
└── data/                    # Data directory
    └── examples/           # Example datasets
```

## Development

```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov

# Format code
poetry run black .
poetry run isort .
```

## Data Structure

Your CSV must include:
1. Region column (configurable in settings)
2. Unique identifier column
3. Additional data columns as needed

Example:
```csv
region,location,data_point,id
Region1,Location1,Value1,1
Region2,Location2,Value2,2
```

## Configuration

Edit `data/config.json`:
```json
{
    "DATA_PATH": "data/your_data.csv",
    "TOKEN_FILE": "data/tokens.csv",
    "FILTER_COLUMN": "region",
    "APP_TITLE": "Data Portal",
    "APP_ICON": "📊"
}
```

## Security Features

- Token-based authentication
- Region-specific data access
- Secure URL parameters
- Admin-only configuration
- Data validation

## Testing Coverage

Run tests with coverage reporting:
```bash
poetry run pytest --cov
```

Coverage report available in `htmlcov/index.html`

## Dependencies

- Python >=3.9
- Streamlit ^1.40.1
- Pandas ^2.2.3
- Additional dependencies in pyproject.toml

## License

MIT License - see [LICENSE](LICENSE)