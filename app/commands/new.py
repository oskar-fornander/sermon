import typer
from app.services.new_sermon import new_sermon


def new():
    """Skapa en ny predikan"""
    new_sermon()

