import typer
from app.services.edit_sermon import interactive_edit_sermon
from app.db import load_sermon_as_draft, create_sermon_from_draft, update_sermon_from_draft, sermon_exists
from app.presentation.common import clear_screen
from app.services.sermon_draft import deep_copy, equal_drafts
from app.presentation.common import console


# sermon edit P371              # interaktivt läge
# sermon edit P371 title "..."  # direktläge


app = typer.Typer(help='Redigera predikan')

@app.callback(invoke_without_command=True)  # Default (interaktiv edit): sermon edit P371
def edit(ctx: typer.Context, sermon_code: str):
    """Interaktiv redigering av en predikan"""

    if not sermon_exists(sermon_code):
        print(f"Predikan med kod {sermon_code} finns inte.")
        return

    ctx.obj = {'sermon_code': sermon_code}  # Make sermon_code available for all sub commands
    if ctx.invoked_subcommand is None:
        clear_screen()
        print(f"interactive edit: {sermon_code}")
        sermon_draft = load_sermon_as_draft(sermon_code)
        #print(sermon_draft)
        original_sermon_draft = deep_copy(sermon_draft)  # original sermon draft without changes
        sermon_draft = interactive_edit_sermon(sermon_draft)  # Launch interactive editor
        #console.print(sermon_draft)
        if sermon_draft:  # Write to database even if no changes were made
            update_sermon_from_draft(sermon_draft)
            console.print(f"Predikan [key]{sermon_code}[/key] är uppdaterad.")
        else:  # None indicates exit edit mode without saving
            console.print(f"Inga ändringar sparade för predikan [key]{sermon_code}[/key].")



