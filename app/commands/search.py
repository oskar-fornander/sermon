
import typer


def search(search_term: str, regex: bool = False, field: str = 'all'):
    """Sök"""
    print(f"Sök på {search_term} i fälten {field} bland predikningarna")

