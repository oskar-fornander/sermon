import typer
from app.services.edit_sermon import interactive_edit_sermon
from app.db import load_sermon_as_draft, create_sermon_from_draft, update_sermon_from_draft, sermon_exists
from app.presentation.common import clear_screen
from app.services.sermon_draft import deep_copy, equal_drafts
from app.presentation.common import console
from app.services.delete_sermon import PendingFileDeletions


# sermon edit P371              # interaktivt läge


def edit(sermon_code: str):
    """Interaktiv redigering av en predikan"""

    if not sermon_exists(sermon_code):
        print(f"Predikan med kod {sermon_code} finns inte.")
        return

    clear_screen()
    print(f"interactive edit: {sermon_code}")
    sermon_draft = load_sermon_as_draft(sermon_code)
    pending_file_deletions = PendingFileDeletions()  # Files waiting for deletion after edit
    #print(sermon_draft)
    original_sermon_draft = deep_copy(sermon_draft)  # original sermon draft without changes
    sermon_draft = interactive_edit_sermon(sermon_draft, pending_file_deletions)  # Launch interactive editor
    #console.print(sermon_draft)
    if sermon_draft:  # Write to database even if no changes were made
        try:
            update_sermon_from_draft(sermon_draft)
            console.print(f"Predikan [key]{sermon_code}[/key] är uppdaterad.")
        except Exception as e:
            console.print(f"Något gick fel vid uppdatering av predikan i databasen ... {e}")

        try:
            pending_file_deletions.execute()  # Now is the time to delete files the user deleted
        except Exception as e:
            console.print(f"Något gick fel vid radering av filer ... {e}")

    else:  # None indicates exit edit mode without saving
        console.print(f"Inga ändringar sparade för predikan [key]{sermon_code}[/key].")



