
from app.presentation.sermon_card import render_sermon_card
from app.services.sermon_draft import load_sermon_as_draft

def show_sermon(sermon_code: str):
    """Show a sermon"""

    sermon_draft = load_sermon_as_draft(sermon_code)
    render_sermon_card(sermon_draft)


