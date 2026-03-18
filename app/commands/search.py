
import typer
from app.presentation.common import clear_screen
from app.services.search_sermons import search_sermons




def search(
        search_term: str, 
        field: str = typer.Option('all', '--field', '-f'), 
        regex: bool = typer.Option(False, '--regex', '-r')):
    """Sök bland predikningarna"""
    print(f"Sök på '{search_term}' bland predikningarna")


    search_sermons(search_term)



