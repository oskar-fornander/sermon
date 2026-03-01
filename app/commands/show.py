import typer
from pathlib import Path
from app.presentation.common import clear_screen
from app.presentation.sermon_card import render_sermon_card
from app.services.sermon_draft import load_sermon_as_draft


def show(sermon_code: str):
    """Visa en specifik predikan (identifierad av sermon-code)"""
    #print(f"Visa predikan {sermon_code}")

    clear_screen()
    sermon_draft = load_sermon_as_draft(sermon_code)

    render_sermon_card(sermon_draft)


