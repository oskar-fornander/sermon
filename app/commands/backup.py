import typer
from app.presentation.common import clear_screen
from app.presentation.common import console
from app.utils import backup_database


# sermon backup   # Makes a backup of the database file

def backup():
    """Gör en backup av aktuell databas"""

    clear_screen()
    backup_file = backup_database()
    console.print(f"Databasen är säkerhetskopierad: [link=file://{backup_file.parent}][link_style]{backup_file.name}[/link_style][/link]")





