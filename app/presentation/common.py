import shutil

from rich.console import Console
from rich.panel import Panel #https://rich.readthedocs.io/en/stable/reference/panel.html
from rich.text import Text
from rich.console import Group
from rich.align import Align
from rich.style import Style
from rich.table import Table
from rich.columns import Columns
from rich import box
from rich.color import Color

from app.presentation.theme import custom_theme

console = Console(theme=custom_theme) #apply custom theme (defined in theme.py) to the console


#width = shutil.get_terminal_size().columns - 4 #Get width of terminal window (with some margin)

