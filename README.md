# Museum Data Crowdsourcing with Streamlit

## Project Overview

This project is a Streamlit-based application designed to allow participants, each associated with a specific country, to view and modify data related to museums in their respective countries. Each participant has a unique token to access their country's data, while administrators can access all data. The data is stored in a CSV file and accessed through a user-friendly interface.

## Table of Contents

1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Token Management](#token-management)
6. [Data Modification](#data-modification)
7. [Contributing](#contributing)
8. [License](#license)
9. [Contact](#contact)

---

## Description

The app enables participants to:

- View museum data specific to their assigned country.
- Modify the data in an editable table.
- Save changes in real-time to a shared dataset.

Administrators can:

- View and modify the entire dataset.
- Distribute token-based URLs to participants.

---

## Installation

### Prerequisites

- [Poetry](https://python-poetry.org/) for dependency management.

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/museum-data-crowdsourcing.git
   cd museum-data-crowdsourcing
   ```

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Place your dataset in the `data` directory (see [Configuration](#configuration)).

4. Generate tokens for participants and administrators (see [Token Management](#token-management)).

---

## Usage

1. Run the Streamlit app:

   ```bash
   poetry run streamlit run app.py
   ```

2. Access the app at `http://localhost:8501/`.

3. Provide participants with token-based URLs:

   ```plaintext
   http://localhost:8501/?token=your_token
   ```

   Replace `your_token` with the token generated in the `tokens.csv` file.

4. Participants can log in using their token to access and modify their data.

---

## Configuration

- **Dataset Path**: Set the path to your CSV file in `config.py` under `DATA_PATH`.
- **Token File**: Define the path to the `tokens.csv` file in `config.py` under `TOKEN_FILE`.
- **Filter Column**: Specify the column used to filter data for participants (e.g., `country_name`) in `config.py` under `FILTER_COLUMN`.
- **General Settings**:
  - `APP_TITLE`: Title of the application.
  - `APP_ICON`: Icon for the application.
  - `HELP_TEXT`: Instructions displayed in the app sidebar.

---

## Token Management

### Generating Tokens

Tokens are used to provide access to specific data for each participant. To generate tokens:

1. Run the token generation script:

   ```bash
   poetry run python generate_tokens.py
   ```

2. The tokens will be saved in a `tokens.csv` file in the `data` directory.

3. Each token is mapped to a specific country or the `admin` role for full access.

### Sharing Tokens

- Share the token-based URL with participants:

  ```plaintext
  http://localhost:8501/?token=your_token
  ```

- Replace `your_token` with the unique token from `tokens.csv`.

---

## Data Modification

Participants can:

- View their filtered dataset based on the assigned token.
- Modify the data directly in an editable table using Streamlit's `data_editor`.
- Save changes, which update the shared dataset in real-time.

Administrators can:

- View and modify the entire dataset using the `admin` token.

---

## Contributing

Contributions are welcome! Please open an issue or pull request if you have suggestions or find bugs.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For questions or inquiries, please contact [your_email@example.com](mailto:your_email@example.com).

---

### Key Changes in This README:
1. **Token Management Section**:
   - Added instructions for generating and sharing tokens.
2. **Usage Update**:
   - Included steps for using token-based URLs.
3. **Configuration Details**:
   - Expanded to include token file and filter column settings.
4. **Enhanced Description**:
   - Clarified participant and administrator roles.