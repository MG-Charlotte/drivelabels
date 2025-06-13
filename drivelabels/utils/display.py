"""
Display utilities for formatting console output.
"""
from typing import List, Dict
from rich.console import Console
from rich.table import Table

from drivelabels.config.settings import TABLE_CONFIG

console = Console()

def display_files(files: List[Dict]) -> List[Dict]:
    """
    Display files in a formatted table with numbers.
    
    Args:
        files (List[Dict]): List of file metadata dictionaries.
        
    Returns:
        List[Dict]: The same list of files for further processing
    """
    table = Table(show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("No.", width=4, justify="right", style="cyan", header_style="bold cyan")
    table.add_column("ID", width=TABLE_CONFIG['id_width'], style="dim")
    table.add_column("Name", width=TABLE_CONFIG['name_width'])
    table.add_column("Type", width=TABLE_CONFIG['type_width'], style="dim")
    table.add_column("Tags", width=TABLE_CONFIG['labels_width'], style="green")
    
    for idx, file in enumerate(files, 1):
        properties = file.get('properties', {})
        tags = properties.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        tag_str = ', '.join(tags) if tags else 'No tags'
        table.add_row(
            f"[cyan]{idx}[/cyan]",
            file['id'],
            file['name'],
            file['mimeType'],
            tag_str
        )
    
    console.print(table)
    return files

def display_menu():
    """Display the main menu options."""
    console.print("\nGoogle Drive Tag Manager")
    console.print("1. List all files")
    console.print("2. Add tag to file")
    console.print("3. Search files by tag")
    console.print("4. Remove tag from file")
    console.print("5. Exit")

def display_success(message: str):
    """
    Display a success message.
    
    Args:
        message (str): The success message to display.
    """
    console.print(f"[green]✓ {message}[/green]")

def display_error(message: str):
    """
    Display an error message.
    
    Args:
        message (str): The error message to display.
    """
    console.print(f"[red]✗ {message}[/red]")

def display_warning(message: str):
    """
    Display a warning message.
    
    Args:
        message (str): The warning message to display.
    """
    console.print(f"[yellow]⚠ {message}[/yellow]") 