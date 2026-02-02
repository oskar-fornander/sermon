import shutil
import os

from rich.console import Console
from rich.panel import Panel #https://rich.readthedocs.io/en/stable/reference/panel.html
from rich.text import Text
from rich.console import Group
from rich.align import Align
from rich.style import Style
from rich.table import Table
from rich.columns import Columns
from rich.padding import Padding
from rich import box
from rich.color import Color
from rich.prompt import Prompt, Confirm

from app.presentation.theme import custom_theme, ICON, LIST_MARKER, TAB

console = Console(theme=custom_theme) #apply custom theme (defined in theme.py) to the console

NBSP = "\u00A0"  # Non breaking space &nbsp;


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def render_info_panel(title: str, content: str='', subtitle: str=''):
    """Renders a small panel with title and maybe content."""
    print()
    console.print(
        Panel(content,
            title=f"[title]{title}[/title]",
            title_align='left', 
            subtitle=subtitle,
            subtitle_align='right',
            box=box.ROUNDED 
        )
    )
    print()


def user_input(title, default=None, choices=None, pattern=None, allow_empty=True, blank_line=True):
    """Custom function to get user input from terminal via rich.prompt() with some safety functions"""
    if blank_line:
        console.print()
    while True:
        answer = Prompt.ask(title, choices=choices, default=default)
        if not answer:
            if allow_empty:
                answer = None  # or ''
                break
            else:
                console.print(f"[bold red]Värdet av [white dim]{title}[/white dim] får inte vara tomt.[/bold red]")
        elif pattern:
            if pattern.match(answer):
                break
            else:
                console.print(f"[bold red]Värdet av [white dim]{title}[/white dim] matchar inte formatet.[/bold red]")
        else:
            break
    #print(f"--{answer}--")
    return answer

def user_confirmation(q, default=True, blank_line=True):
    """Prompt user for confirmation before moving on."""
    if blank_line:
        console.print()
    answer = Confirm.ask(q, default=default)
    return answer

def user_choice(title='Ditt val', options = None, default = None):
    """Wait for user to make a choice (from a list of options)"""
    
    while True:
        choice = Prompt.ask(title, default=default)
        if not choice:
            continue  # empty choice is not an option
            #return False  # empty choice
        if options:
            if choice.strip() not in options:
                console.print(f"[bold red]Välj ett av alternativen ([white dim]{', '.join(options)}[/white dim]).[/bold red]")
                continue
        return choice





