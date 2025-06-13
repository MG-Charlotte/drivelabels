import os
import pickle
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.labels'
]

class DriveLabelManager:
    def __init__(self):
        self.console = Console()
        self.creds = None
        self.drive_service = None
        self.labels_service = None
        self.folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        
    def authenticate(self):
        """Handles OAuth2 authentication with Google Drive."""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.labels_service = build('drivelabels', 'v2', credentials=self.creds)
    
    def list_files(self) -> List[Dict]:
        """Lists all files in the specified folder with their metadata."""
        try:
            results = self.drive_service.files().list(
                q=f"'{self.folder_id}' in parents",
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, labels)"
            ).execute()
            return results.get('files', [])
        except HttpError as error:
            self.console.print(f"[red]An error occurred: {error}[/red]")
            return []

    def add_label(self, file_id: str, label_name: str):
        """Adds a label to a file."""
        try:
            # First, get or create the label
            label = self._get_or_create_label(label_name)
            
            # Apply the label to the file
            self.drive_service.files().modifyLabels(
                fileId=file_id,
                body={
                    'labelModifications': [{
                        'labelId': label['id'],
                        'fieldModifications': [{
                            'fieldId': label['fields'][0]['id'],
                            'setSelection': {
                                'values': [label['fields'][0]['id']]
                            }
                        }]
                    }]
                }
            ).execute()
            
            self.console.print(f"[green]Label '{label_name}' added successfully![/green]")
                
        except HttpError as error:
            self.console.print(f"[red]An error occurred: {error}[/red]")

    def _get_or_create_label(self, label_name: str) -> Dict:
        """Gets an existing label or creates a new one."""
        try:
            # Try to find existing label
            labels = self.labels_service.labels().list().execute()
            for label in labels.get('labels', []):
                if label['name'] == label_name:
                    return label
            
            # Create new label if not found
            label = self.labels_service.labels().create(
                body={
                    'name': label_name,
                    'labelType': 'USER',
                    'fields': [{
                        'id': f'{label_name}_field',
                        'type': 'SELECTION',
                        'properties': {
                            'displayName': label_name,
                            'selectionOptions': [{
                                'id': f'{label_name}_option',
                                'properties': {
                                    'displayName': label_name
                                }
                            }]
                        }
                    }]
                }
            ).execute()
            return label
            
        except HttpError as error:
            self.console.print(f"[red]An error occurred: {error}[/red]")
            raise

    def search_by_label(self, label_name: str) -> List[Dict]:
        """Searches for files with a specific label."""
        try:
            label = self._get_or_create_label(label_name)
            results = self.drive_service.files().list(
                q=f"'{self.folder_id}' in parents and labels contains '{label['id']}'",
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, labels)"
            ).execute()
            return results.get('files', [])
        except HttpError as error:
            self.console.print(f"[red]An error occurred: {error}[/red]")
            return []

    def display_files(self, files: List[Dict]):
        """Displays files in a formatted table."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", width=44)  # Google Drive IDs are 44 characters long
        table.add_column("Name", width=30)
        table.add_column("Type", width=30)
        table.add_column("Labels", width=20)
        
        for file in files:
            labels = file.get('labels', {})
            label_names = [label for label in labels.keys() if labels[label]]
            label_str = ', '.join(label_names) if label_names else 'No labels'
            table.add_row(
                file['id'],
                file['name'],
                file['mimeType'],
                label_str
            )
        
        self.console.print(table)

def main():
    manager = DriveLabelManager()
    manager.authenticate()
    
    while True:
        manager.console.print("\n[bold cyan]Google Drive Label Manager[/bold cyan]")
        manager.console.print("1. List all files")
        manager.console.print("2. Add label to file")
        manager.console.print("3. Search files by label")
        manager.console.print("4. Exit")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            files = manager.list_files()
            manager.display_files(files)
            
        elif choice == "2":
            files = manager.list_files()
            manager.display_files(files)
            file_id = Prompt.ask("Enter the file ID to label")
            label = Prompt.ask("Enter the label to add")
            manager.add_label(file_id, label)
            
        elif choice == "3":
            label = Prompt.ask("Enter the label to search for")
            files = manager.search_by_label(label)
            manager.display_files(files)
            
        elif choice == "4":
            break
        
        time.sleep(1)  # Prevent rate limiting

if __name__ == '__main__':
    main() 