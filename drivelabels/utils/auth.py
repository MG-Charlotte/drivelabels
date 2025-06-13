"""
Authentication utilities for Google Drive API.
"""
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

from drivelabels.config.settings import SCOPES, API_CONFIG

def get_credentials():
    """
    Get or refresh Google API credentials.
    
    Returns:
        Credentials: The OAuth2 credentials object.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_services(creds):
    """
    Initialize Google API services.
    
    Args:
        creds (Credentials): OAuth2 credentials object.
    
    Returns:
        tuple: (drive_service, labels_service) Google API service objects.
    """
    drive_service = build(
        API_CONFIG['drive']['service'],
        API_CONFIG['drive']['version'],
        credentials=creds
    )
    
    labels_service = build(
        API_CONFIG['labels']['service'],
        API_CONFIG['labels']['version'],
        credentials=creds
    )
    
    return drive_service, labels_service 