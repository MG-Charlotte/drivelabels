# Google Drive Label Manager

A Python application that allows you to manage custom tags for files in a specific Google Drive folder.

## Features

- OAuth2 authentication with Google Drive
- List files in a specific folder
- Add custom tags to files
- Search files by tags
- Beautiful command-line interface
- Rate limit handling

## Prerequisites

- Python 3.9 or higher
- Google Cloud Platform account
- Google Drive API enabled

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
   - Enable the Google Drive API
   - Create OAuth 2.0 credentials
   - Download the credentials and save as `credentials.json` in the project directory

4. Create a `.env` file with your Google Drive folder ID:

```
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
```

## Usage

1. Run the application:

```bash
python drive_labels.py
```

2. On first run, you'll be prompted to authenticate with Google Drive in your browser.

3. Use the menu options to:
   - List all files in the folder
   - Add tags to files
   - Search files by tags

## Notes

- The application stores authentication tokens in `token.pickle`
- Tags are stored as custom properties in Google Drive
- Rate limiting is handled with a 1-second delay between operations
