#app/services/export_podcast.py

from app.utils import parse_sermon_code
from app.services.sermon_draft import load_sermon_as_draft
from app.presentation.common import console





def export_podcast(sermon_code: str):
    """Export sermon to podcast."""

    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format or raise error

    sermon_draft = load_sermon_as_draft(sermon_code)


    console.print('TODO: Skriv kod för att exportera som podcast.')





