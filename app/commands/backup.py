import typer
from app.presentation.common import clear_screen
from app.presentation.common import console
from app.utils import backup_database


# sermon backup   # Makes a backup of the database file

def backup():
    """Gör en backup av aktuell databas"""

    backup_file = backup_database()
    console.print(f"Databasen är säkerhetskopierad: {backup_file}")





