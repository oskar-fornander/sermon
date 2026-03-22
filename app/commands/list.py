import typer
from typing import Optional, Literal
from app.services.list_sermons import list_sermons
from app.presentation.common import clear_screen
from app.errors import ValidationError

app = typer.Typer(help = 'Lista de senaste predikningarna', invoke_without_command=True)
#   sermon list [--limit N] [--all] [--date] [--reverse]

@app.callback()
def sermon_listing_function(
        limit: int = typer.Option(10, '--limit', '-n', help='Antal predikningar att visa'),
        all: bool = typer.Option(False, '--all', help='Visa alla predikningar'), 
        #sort: str = typer.Option("code", "--sort", help="Sortera efter predikokod 'code' eller datum 'date'"),
        sort: Literal['code', 'date'] = typer.Option('code', '--sort', help="Sortera efter predikokod 'code' eller datum 'date'"),
        reverse: bool = typer.Option(False, '--reverse', '-r', help='Omvänd sortering'),

        year: Optional[int] = typer.Option(None, '--year', help='Filtrera efter år'),
        month: Optional[str] = typer.Option(None, '--month', help='Filtrera efter månad'),
        place: Optional[str] = typer.Option(None, '--place', help='Filtrera efter plats'),
        report: Optional[str] = typer.Option(None, '--report', help='Filtrera efter omdöme (A, B, C)'),
        has_recording: bool = typer.Option(None, '--has-recording', help='Visa endast predikningar med inspelning')
        ):

    """Lista alla eller några av predikningarna"""

    clear_screen()
    
    if all:
        limit = 0  # Display all

    if sort == 'date':
        list_sermons(list_by='date', n=limit, reverse=reverse, year=year, month=month, place=place, report=report, must_have_recording=has_recording)  # List sermons by service dates
    else:
        list_sermons(list_by='code', n=limit, reverse=reverse, year=year, month=month, place=place, report=report, must_have_recording=has_recording)  # List sermons by sermon code


