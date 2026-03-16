import typer
from pathlib import Path
from app.presentation.common import clear_screen
from app.services.show_sermon import show_sermon


def show(sermon_code: str):
    """Visa en predikan"""
    #print(f"Visa predikan {sermon_code}")

    clear_screen()
    show_sermon(sermon_code)



