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
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class DriveLabelManager:
    def __init__(self):
        self.console = Console()
        self.creds = None
        self.service = None
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
        
        self.service = build('drive', 'v3', credentials=self.creds)
    
    def list_files(self) -> List[Dict]:
        """Lists all files in the specified folder with their metadata."""
        try:
            results = self.service.files().list(
                q=f"'{self.folder_id}' in parents",
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, properties)"
            ).execute()
            return results.get('files', [])
        except HttpError as error:
            self.console.print(f"[red]An error occurred: {error}[/red]")
            return []

    def add_tag(self, file_id: str, tag: str):
        """Adds a custom tag to a file's properties."""
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='properties'
            ).execute()
            
            properties = file.get('properties', {})
            tags = properties.get('tags', '').split(',')
            tags = [t.strip() for t in tags if t.strip()]
            
            if tag not in tags:
                tags.append(tag)
                properties['tags'] = ','.join(tags)
                
                self.service.files().update(
                    fileId=file_id,
                    body={'properties': properties},
                    fields='properties'
                ).execute()
                
                self.console.print(f"[green]Tag '{tag}' added successfully![/green]")
            else:
                self.console.print(f"[yellow]Tag '{tag}' already exists![/yellow]")
                
        except HttpError as error:
            self.console.print(f"[red]An error occurred: {error}[/red]")

    def search_by_tag(self, tag: str) -> List[Dict]:
        """Searches for files with a specific tag."""
        try:
            results = self.service.files().list(
                q=f"'{self.folder_id}' in parents and properties has {{ key='tags' and value contains '{tag}' }}",
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, properties)"
            ).execute()
            return results.get('files', [])
        except HttpError as error:
            self.console.print(f"[red]An error occurred: {error}[/red]")
            return []

    def display_files(self, files: List[Dict]):
        """Displays files in a formatted table."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name")
        table.add_column("Type")
        table.add_column("Tags")
        
        for file in files:
            properties = file.get('properties', {})
            tags = properties.get('tags', 'No tags')
            table.add_row(
                file['name'],
                file['mimeType'],
                tags
            )
        
        self.console.print(table)

def main():
    manager = DriveLabelManager()
    manager.authenticate()
    
    while True:
        manager.console.print("\n[bold cyan]Google Drive Label Manager[/bold cyan]")
        manager.console.print("1. List all files")
        manager.console.print("2. Add tag to file")
        manager.console.print("3. Search files by tag")
        manager.console.print("4. Exit")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            files = manager.list_files()
            manager.display_files(files)
            
        elif choice == "2":
            files = manager.list_files()
            manager.display_files(files)
            file_id = Prompt.ask("Enter the file ID to tag")
            tag = Prompt.ask("Enter the tag to add")
            manager.add_tag(file_id, tag)
            
        elif choice == "3":
            tag = Prompt.ask("Enter the tag to search for")
            files = manager.search_by_tag(tag)
            manager.display_files(files)
            
        elif choice == "4":
            break
        
        time.sleep(1)  # Prevent rate limiting

if __name__ == '__main__':
    main() 