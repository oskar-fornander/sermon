
import typer
from typing import Optional, Literal, List
from app.presentation.common import clear_screen
from app.services.search_sermons import search_sermons


# No search with regular expressions.
# Implement in the future? 
#   sermon search tro hopp -kärlek => tro AND hopp AND NOT kärlek
#   sermon search title:nåd - probably not.



def search(
        #query: str, 
        query: List[str] = typer.Argument(),
        bible_only: bool = typer.Option(False, '--bible', help='Sök endast bland bibelreferenser'),
        limit: int = typer.Option(0, '--limit', '-n', help='Begränsa sökresultatet till antal predikningar (0 = ingen begränsning)'),
        date_from: str = typer.Option('', '--from', help='Visa predikningar senare än detta datum'),
        date_to: str = typer.Option('', '--to', help='Visa predikningar före detta datum'),
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

    if sort == 'date':
        search_sermons(query=query, list_by='date', n=limit, reverse=reverse, bible_only=bible_only, date_from=date_from, date_to=date_to, year=year, month=month, place=place, report=report, must_have_recording=has_recording)  # List sermons by service dates
    else:
        search_sermons(query=query, list_by='code', n=limit, reverse=reverse, bible_only=bible_only, date_from=date_from, date_to=date_to, year=year, month=month, place=place, report=report, must_have_recording=has_recording)  # List sermons by sermon code

