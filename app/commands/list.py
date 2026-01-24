import typer
from app.services.list_sermons import list_sermons_by_code, list_sermons_by_date
from app.presentation.common import clear_screen


app = typer.Typer(help = 'Lista de senaste predikningarna', invoke_without_command=True)
#   sermon list [--limit N] [--all] [--date] [--reverse]

@app.callback()
def sermon_listing_function(
        limit: int = typer.Option(3, '--limit', '-n', help='Antal predikningar att visa'),
        all: bool = typer.Option(False, '--all', help='Visa alla predikningar'), 
        date: bool = typer.Option(False, '--date', help='Sorterat efter datum för framförande istället för kod'),
        reverse: bool = typer.Option(False, '--reverse', '-r', help='Omvänd sortering')):
    """Lista alla eller några av predikningarna"""

    clear_screen()
    
    if not all:  # How many to display?
        n = limit
    else:
        n = 0

    if date:
        list_sermons_by_date(n=n, reverse=reverse)  #List sermons by service dates
    else:
        list_sermons_by_code(n=n, reverse=reverse)  #List sermons by code, e.g. P372


