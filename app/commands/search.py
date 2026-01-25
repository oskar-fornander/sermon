
import typer
from app.presentation.common import clear_screen


def search(search_term: str, field: str = typer.Option('all', '--field', '-f'), regex: bool = typer.Option(False, '--regex', '-r')):
    """Sök"""
    print(f"Sök på {search_term} i fälten {field} bland predikningarna")

