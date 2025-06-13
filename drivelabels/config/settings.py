"""
Configuration settings for the Drive Labels application.
"""
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# OAuth2 scopes required for the application
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.labels'
]

# Google Drive folder ID to monitor
FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

# API configuration
API_CONFIG = {
    'drive': {
        'version': 'v3',
        'service': 'drive'
    },
    'labels': {
        'version': 'v2',
        'service': 'drivelabels'
    }
}

# Table display configuration
TABLE_CONFIG = {
    'id_width': 44,  # Google Drive IDs are 44 characters long
    'name_width': 30,
    'type_width': 30,
    'labels_width': 20
}

# Logging configuration
LOG_FILE = 'drivelabels.log'
LOG_LEVEL = logging.INFO

logging.basicConfig(
    filename=LOG_FILE,
    level=LOG_LEVEL,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
) 