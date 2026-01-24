import typer
from app.utils import CONFIG, ARCHIVE_ROOT
from pathlib import Path
from app.presentation.sermon_card import render_sermon_card
from app.db import load_sermon_as_draft


def show(sermon_code: str):
    """Visa en specifik predikan (identifierad av sermon-code)"""
    #print(f"Visa predikan {sermon_code}")

    sermon_draft = load_sermon_as_draft(sermon_code)

    if not sermon_draft:
        print(f"Predikan med kod {sermon_code} finns inte.")
        return

    render_sermon_card(sermon_draft)


