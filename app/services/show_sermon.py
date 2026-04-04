
from app.presentation.sermon_card import render_sermon_card
from app.services.sermon_draft import load_sermon_as_draft
from app.utils import parse_sermon_code

def show_sermon(sermon_code: str):
    """Show a sermon"""

    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format or raise error

    sermon_draft = load_sermon_as_draft(sermon_code)
    render_sermon_card(sermon_draft)


