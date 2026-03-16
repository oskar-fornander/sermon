import typer
from app.errors import *
from app.services.edit_sermon import edit_sermon
from app.presentation.common import clear_screen
from app.presentation.common import console


# sermon edit P371              # interaktivt läge


def edit(sermon_code: str):
    """Redigera data för en predikan"""
    clear_screen()
    edit_sermon(sermon_code)

