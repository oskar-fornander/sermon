
import typer
from typing import Optional, Literal
from app.presentation.common import clear_screen
from app.services.search_sermons import search_sermons


# No search with regular expressions.
# Implement in the future? 
#   sermon search title:nåd
#   Search multiple words with AND: sermon search "nåd tro" -> nåd AND tro



def search(
        search_term: str, 
        limit: int = typer.Option(10, '--limit', '-n', help='Antal predikningar att visa'),
        all: bool = typer.Option(True, '--all', help='Visa alla predikningar'), 
        offset: int = typer.Option(0, '--offset', help='Offset från senaste predikan'),
        #sort: str = typer.Option("code", "--sort", help="Sortera efter predikokod 'code' eller datum 'date'"),
        sort: Literal['code', 'date'] = typer.Option('code', '--sort', help="Sortera efter predikokod 'code' eller datum 'date'"),
        reverse: bool = typer.Option(False, '--reverse', '-r', help='Omvänd sortering'),

        year: Optional[int] = typer.Option(None, '--year', help='Filtrera efter år'),
        month: Optional[str] = typer.Option(None, '--month', help='Filtrera efter månad'),
        place: Optional[str] = typer.Option(None, '--place', help='Filtrera efter plats'),
        report: Optional[str] = typer.Option(None, '--report', help='Filtrera efter omdöme (A, B, C)'),
        has_recording: bool = typer.Option(None, '--has-recording', help='Visa endast predikningar med inspelning')
        ):

    """Sök bland predikningarna"""

    clear_screen()
    print(f"Sök på '{search_term}' bland predikningarna")

    if all:
        limit = 0  # Display all
        offset = 0  # No offset in search

    if sort == 'date':
        search_sermons(search_term=search_term, list_by='date', n=limit, offset=offset, reverse=reverse, year=year, month=month, place=place, report=report, must_have_recording=has_recording)  # List sermons by service dates
    else:
        search_sermons(search_term=search_term, list_by='code', n=limit, offset=offset, reverse=reverse, year=year, month=month, place=place, report=report, must_have_recording=has_recording)  # List sermons by sermon code



