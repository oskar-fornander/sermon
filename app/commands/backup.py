import typer
from app.presentation.common import clear_screen
from app.presentation.common import console
from app.utils import backup_database


# sermon backup   # Makes a backup of the database file

def backup():
    """Gör en backup av aktuell databas"""

    if backup_database():
        console.print(f"Databasen är säkerhetskopierad.")
    else:
        console.print(f"Ett fel uppstod vid säkerhetskopiering av databasen.")





