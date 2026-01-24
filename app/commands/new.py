import typer
from app.services.new_sermon import new_sermon
from app.presentation.common import clear_screen


def new():
    """Skapa en ny predikan"""
    clear_screen()
    new_sermon()

