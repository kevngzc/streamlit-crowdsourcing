# CSV Crowdsourcing Platform

A Streamlit-based platform for collaborative data management with region-specific access control. Perfect for distributed data collection or validation across different regions, departments, or organizational units.

## 🎯 Features

- **Region-Specific Access**: Users can only view and edit data for their assigned region
- **Token-Based Authentication**: Secure access control using unique tokens
- **Admin Dashboard**: Full data management and configuration capabilities
- **Real-Time Editing**: Direct data modification with immediate updates
- **Excel Export**: Download token data in Excel format
- **Flexible Data Structure**: Works with any CSV format that includes a region column

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Poetry for dependency management

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/csv-crowdsourcing.git
cd csv-crowdsourcing
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Prepare your data structure:
```bash
data/
├── your_data.csv    # Your CSV data with region column
└── tokens.csv       # Generated access tokens
```

4. Set up configuration in `config.json`:
```json
{
    "DATA_PATH": "data/your_data.csv",
    "TOKEN_FILE": "data/tokens.csv",
    "FILTER_COLUMN": "your_region_column",
    "APP_TITLE": "Data Update Portal",
    "APP_ICON": "📊",
    "HELP_TEXT": "### How to use the app:\n1. Enter your token on the home page.\n2. If valid, view the filtered data for your region.\n3. Edit values directly in the table.\n4. Save your changes when done!"
}
```

### Getting Started

1. Generate access tokens:
```bash
poetry run python generate_tokens.py
```

2. Launch the application:
```bash
poetry run streamlit run app.py
```

3. Access via your browser:
- Local: `http://localhost:8501`
- Token URL: `http://localhost:8501/?token=YOUR_TOKEN`

## 📊 Data Structure

Your CSV data must include:
1. A region/filtering column (specified in `FILTER_COLUMN`)
2. Any additional data columns you need
3. A unique identifier column

Example formats:

```csv
# Example 1: Geographic Data
region_name,location,data_point,timestamp,id

# Example 2: Organizational Data
department,employee_id,project,status,comments,record_id
```

## 💼 Admin Features

The admin interface provides:
1. **Dataset Management**:
   - Upload new CSV data
   - Replace or append to existing data
   - Preview data before importing

2. **Token Management**:
   - View all active tokens
   - Download token list as Excel
   - Monitor token assignments

3. **Configuration**:
   - Update application settings
   - Customize app title and icon
   - Modify help text
   - Change data paths

## 👥 User Features

Users can:
1. Access via token or URL
2. View and edit their region's data
3. Save changes in real-time
4. Navigate easily with home button
5. Log out securely

## 🔒 Security Features

- Token-based authentication
- Region-specific data access
- Secure URL parameters
- Admin-only configuration
- Safe data handling

## 📁 Project Structure
```
project/
├── app.py                # Main application
├── generate_tokens.py    # Token generation
├── config.json          # Configuration
├── data/               
│   ├── your_data.csv    # Data file
│   └── tokens.csv       # Access tokens
├── style.css            # Custom styling
└── README.md           
```

## ⚙️ Configuration Options

| Setting | Description | Example |
|---------|-------------|---------|
| DATA_PATH | Path to data CSV | "data/your_data.csv" |
| TOKEN_FILE | Path to tokens CSV | "data/tokens.csv" |
| FILTER_COLUMN | Column for filtering | "region_name" |
| APP_TITLE | Application title | "Data Portal" |
| APP_ICON | Emoji icon | "📊" |
| HELP_TEXT | Sidebar help text | "### How to use..." |

## 🔄 Best Practices

1. **Data Management**:
   - Regular backups
   - Validate CSV structure
   - Use clear column names
   - Include unique IDs

2. **Token Management**:
   - Secure distribution
   - Regular rotation
   - Clear assignments
   - Excel export for tracking

3. **User Access**:
   - Share token URLs
   - Monitor usage
   - Review permissions
   - Regular audits

## 🛠️ Development

### Adding Features

1. Update `app.py` for new functionality
2. Modify `style.css` for styling
3. Update `config.json` for settings

### Requirements

```toml
[tool.poetry.dependencies]
python = "^3.9"
streamlit = "^1.29.0"
pandas = "^2.1.0"
xlsxwriter = "^3.1.9"
```

## 🆘 Support

1. Check Help text in sidebar
2. Review configuration
3. Contact administrator
4. Create GitLab issue

## 📝 License

MIT License - see [LICENSE](LICENSE)