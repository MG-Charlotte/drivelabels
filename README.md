# Google Drive Label Manager

A Python application that allows you to manage labels for files in a specific Google Drive folder.

## Features

- OAuth2 authentication with Google Drive
- List files in a specific folder
- Add custom labels to files
- Search files by labels
- Beautiful command-line interface
- Rate limit handling
- Modular code structure for easy maintenance

## Project Structure

```
drivelabels/
├── config/
│   └── settings.py      # Configuration settings
├── core/
│   └── drive_manager.py # Core Drive operations
├── utils/
│   ├── auth.py         # Authentication utilities
│   └── display.py      # Display formatting utilities
├── __init__.py         # Package initialization
└── main.py            # Application entry point
```

## Prerequisites

- Python 3.9 or higher
- Google Cloud Platform account
- Google Drive API enabled
- Google Drive Labels API enabled

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up Google Cloud Project:

   - Go to the [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable the Google Drive API and Drive Labels API
   - Create OAuth 2.0 credentials
   - Download the credentials and save as `credentials.json` in the project directory

4. Create a `.env` file with your Google Drive folder ID:

```
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
```

## Usage

1. Run the application:

```bash
python main.py
```

2. On first run, you'll be prompted to authenticate with Google Drive in your browser.

3. Use the menu options to:
   - List all files in the folder
   - Add labels to files
   - Search files by labels

## Development

The application is structured in a modular way:

- `config/settings.py`: Contains all configuration settings
- `core/drive_manager.py`: Core Drive operations and label management
- `utils/auth.py`: Authentication and service initialization
- `utils/display.py`: Console output formatting
- `main.py`: Application entry point and menu handling

## Notes

- The application stores authentication tokens in `token.pickle`
- Labels are stored using Google Drive's native labeling system
- Rate limiting is handled with a 1-second delay between operations
- All sensitive files (`.env`, `credentials.json`, `token.pickle`) are git-ignored
