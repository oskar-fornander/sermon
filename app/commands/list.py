import typer
from typing import Optional, Literal
from app.services.list_sermons import list_sermons
from app.presentation.common import clear_screen
from app.errors import ValidationError

default_limit = 10  # How many sermons to list

app = typer.Typer(help = 'Lista de senaste predikningarna', invoke_without_command=True)
#   sermon list [--limit N] [--all] [--date] [--reverse]

@app.callback()
def sermon_listing_function(
        limit: int = typer.Option(default_limit, '--limit', '-n', help='Antal predikningar att visa'),
        all: bool = typer.Option(False, '--all', help='Visa alla predikningar'), 
        date_from: str = typer.Option('', '--from', help='Visa predikningar senare än detta datum'),
        date_to: str = typer.Option('', '--to', help='Visa predikningar före detta datum'),
        sort: Literal['code', 'date'] = typer.Option('code', '--sort', help="Sortera efter predikokod 'code' eller datum 'date'"),
        reverse: bool = typer.Option(False, '--reverse', '-r', help='Omvänd sortering'),

        date: Optional[str] = typer.Option(None, '--date', help='Filtrera efter datum YYYY-MM-DD'),
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
        list_sermons(list_by='date', n=limit, reverse=reverse, date=date, date_from=date_from, date_to=date_to, year=year, month=month, place=place, report=report, must_have_recording=has_recording)  # List sermons by service dates
    else:
        list_sermons(list_by='code', n=limit, reverse=reverse, date=date, date_from=date_from, date_to=date_to, year=year, month=month, place=place, report=report, must_have_recording=has_recording)  # List sermons by sermon code


