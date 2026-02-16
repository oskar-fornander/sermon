import typer
from app.services.delete_sermon import delete_sermon
from app.presentation.common import clear_screen
from app.presentation.common import console
from app.db import sermon_exists

# sermon delete P371

def delete(sermon_code: str):
    """Radera en predikan och alla tillhörande filer"""

    if not sermon_exists(sermon_code):
        print(f"Predikan med kod {sermon_code} finns inte.")
        return

    delete_sermon(sermon_code)


