"""
Core Drive Manager class for handling Google Drive operations.
"""
from typing import List, Dict
from googleapiclient.errors import HttpError

from drivelabels.config.settings import FOLDER_ID
from drivelabels.utils.display import display_error

class DriveManager:
    """Manages Google Drive operations including file listing and tag management."""
    
    def __init__(self, drive_service, labels_service):
        """
        Initialize the Drive Manager.
        
        Args:
            drive_service: Google Drive API service instance
            labels_service: Google Drive Labels API service instance (kept for future use)
        """
        self.drive_service = drive_service
        self.labels_service = labels_service
    
    def list_files(self) -> List[Dict]:
        """
        List all files in the specified folder.
        
        Returns:
            List[Dict]: List of file metadata dictionaries.
        """
        try:
            results = self.drive_service.files().list(
                q=f"'{FOLDER_ID}' in parents",
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, properties)"
            ).execute()
            return results.get('files', [])
        except HttpError as error:
            display_error(f"An error occurred: {error}")
            return []

    def add_tag(self, file_id: str, tag_name: str) -> bool:
        """
        Add a tag to a file using custom properties.
        
        Args:
            file_id (str): The ID of the file to tag
            tag_name (str): The name of the tag to add
            
        Returns:
            bool: True if tag was added successfully, False otherwise
        """
        try:
            # Get current properties
            file = self.drive_service.files().get(
                fileId=file_id,
                fields='properties'
            ).execute()
            
            # Get existing tags or initialize empty list
            current_tags = file.get('properties', {}).get('tags', '').split(',')
            current_tags = [tag.strip() for tag in current_tags if tag.strip()]
            
            # Add new tag if not already present
            if tag_name not in current_tags:
                current_tags.append(tag_name)
                
                # Update file properties
                self.drive_service.files().update(
                    fileId=file_id,
                    body={
                        'properties': {
                            'tags': ','.join(current_tags)
                        }
                    },
                    fields='properties'
                ).execute()
                
                return True
            return False
                
        except HttpError as error:
            display_error(f"An error occurred: {error}")
            return False

    def search_by_tag(self, tag_name: str) -> List[Dict]:
        """
        Search for files with a specific tag.
        
        Args:
            tag_name (str): The name of the tag to search for
            
        Returns:
            List[Dict]: List of file metadata dictionaries
        """
        try:
            # List all files and filter by tag
            results = self.drive_service.files().list(
                q=f"'{FOLDER_ID}' in parents",
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, properties)"
            ).execute()
            
            files = results.get('files', [])
            tagged_files = []
            
            for file in files:
                properties = file.get('properties', {})
                tags = properties.get('tags', '').split(',')
                tags = [tag.strip() for tag in tags if tag.strip()]
                
                if tag_name in tags:
                    tagged_files.append(file)
            
            return tagged_files
            
        except HttpError as error:
            display_error(f"An error occurred: {error}")
            return []

    def remove_tag(self, file_id: str, tag_name: str) -> bool:
        """
        Remove a tag from a file.
        
        Args:
            file_id (str): The ID of the file to remove the tag from
            tag_name (str): The name of the tag to remove
            
        Returns:
            bool: True if tag was removed successfully, False otherwise
        """
        try:
            # Get current properties
            file = self.drive_service.files().get(
                fileId=file_id,
                fields='properties'
            ).execute()
            
            # Get existing tags
            current_tags = file.get('properties', {}).get('tags', '').split(',')
            current_tags = [tag.strip() for tag in current_tags if tag.strip()]
            
            # Remove tag if present
            if tag_name in current_tags:
                current_tags.remove(tag_name)
                
                # Update file properties
                self.drive_service.files().update(
                    fileId=file_id,
                    body={
                        'properties': {
                            'tags': ','.join(current_tags) if current_tags else ''
                        }
                    },
                    fields='properties'
                ).execute()
                
                return True
            return False
                
        except HttpError as error:
            display_error(f"An error occurred: {error}")
            return False 