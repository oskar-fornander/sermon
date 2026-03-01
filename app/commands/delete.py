import typer
from app.services.delete_sermon import delete_sermon
from app.presentation.common import clear_screen
from app.presentation.common import console

# sermon delete P371

def delete(sermon_code: str):
    """Radera en predikan och alla tillhörande filer"""
    clear_screen()
    delete_sermon(sermon_code)


