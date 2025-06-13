"""
Main entry point for the Drive Labels application.
"""
import time
import traceback
import logging
from rich.prompt import Prompt, IntPrompt
from rich.console import Console

from drivelabels.utils.auth import get_credentials, get_services
from drivelabels.core.drive_manager import DriveManager
from drivelabels.utils.display import (
    display_menu,
    display_files,
    display_success,
    display_error,
    display_warning
)

console = Console()

def get_file_by_number(files: list, prompt: str = "Enter file number") -> dict:
    """
    Get a file by its number in the displayed list.
    
    Args:
        files (list): List of file dictionaries
        prompt (str): Prompt message for user input
        
    Returns:
        dict: Selected file dictionary
    """
    while True:
        try:
            num = IntPrompt.ask(prompt, default=1)
            if 1 <= num <= len(files):
                return files[num - 1]
            display_error(f"Please enter a number between 1 and {len(files)}")
        except ValueError:
            display_error("Please enter a valid number")

def display_available_tags(tags: list):
    """Display a numbered list of available tags."""
    console.print("\nAvailable tags:")
    for idx, tag in enumerate(tags, 1):
        console.print(f"[cyan]{idx}[/cyan]. {tag}")

def main():
    """Main application entry point."""
    logger = logging.getLogger("main")
    try:
        # Initialize services
        creds = get_credentials()
        drive_service, labels_service = get_services(creds)
        logger.info("Initialized Google API services.")
        
        # Initialize drive manager
        manager = DriveManager(drive_service, labels_service)
        logger.info("DriveManager initialized.")
        
        while True:
            try:
                display_menu()
                choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"])
                logger.info(f"User selected menu option: {choice}")
                
                if choice == "1":
                    files = display_files(manager.list_files())
                    logger.info(f"Listed {len(files)} files.")
                    
                elif choice == "2":
                    files = display_files(manager.list_files())
                    if not files:
                        display_warning("No files found in the folder.")
                        continue
                        
                    selected_file = get_file_by_number(files, "Enter the number of the file to tag")
                    tag = Prompt.ask("Enter the tag to add")
                    
                    logger.info(f"Attempting to add tag '{tag}' to file '{selected_file['name']}'")
                    if manager.add_tag(selected_file['id'], tag):
                        display_success(f"Tag '{tag}' added successfully to '{selected_file['name']}'!")
                        logger.info(f"Tag '{tag}' added to file '{selected_file['id']}'.")
                    else:
                        display_error(f"Failed to add tag '{tag}'.")
                        logger.error(f"Failed to add tag '{tag}' to file '{selected_file['id']}'.")
                    
                elif choice == "3":
                    tag = Prompt.ask("Enter the tag to search for")
                    files = display_files(manager.search_by_tag(tag))
                    logger.info(f"Searched for files with tag '{tag}'. Found {len(files)} files.")
                
                elif choice == "4":
                    files = display_files(manager.list_files())
                    if not files:
                        display_warning("No files found in the folder.")
                        continue
                        
                    selected_file = get_file_by_number(files, "Enter the number of the file to remove tag from")
                    
                    # Get current tags
                    properties = selected_file.get('properties', {})
                    tags = properties.get('tags', '').split(',')
                    tags = [tag.strip() for tag in tags if tag.strip()]
                    
                    if not tags:
                        display_warning(f"File '{selected_file['name']}' has no tags.")
                        continue
                    
                    # Display available tags
                    display_available_tags(tags)
                    
                    # Get tag to remove
                    tag_num = IntPrompt.ask("Enter the number of the tag to remove", default=1)
                    if 1 <= tag_num <= len(tags):
                        tag_to_remove = tags[tag_num - 1]
                        logger.info(f"Attempting to remove tag '{tag_to_remove}' from file '{selected_file['name']}'")
                        
                        if manager.remove_tag(selected_file['id'], tag_to_remove):
                            display_success(f"Tag '{tag_to_remove}' removed successfully from '{selected_file['name']}'!")
                            logger.info(f"Tag '{tag_to_remove}' removed from file '{selected_file['id']}'.")
                        else:
                            display_error(f"Failed to remove tag '{tag_to_remove}'.")
                            logger.error(f"Failed to remove tag '{tag_to_remove}' from file '{selected_file['id']}'.")
                    else:
                        display_error(f"Please enter a number between 1 and {len(tags)}")
                    
                elif choice == "5":
                    display_success("Exiting application. Goodbye!")
                    logger.info("User exited the application.")
                    break
                
                time.sleep(1)  # Prevent rate limiting
            except KeyboardInterrupt:
                display_error("Interrupted by user. Exiting application.")
                logger.warning("Application interrupted by user (KeyboardInterrupt).")
                break
            except Exception as e:
                display_error(f"Unexpected error: {e}")
                logger.exception(f"Unexpected error: {e}")
    except Exception as e:
        display_error(f"Fatal error: {e}")
        logger.critical(f"Fatal error: {e}", exc_info=True)

if __name__ == '__main__':
    main() 