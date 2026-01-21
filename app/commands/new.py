import typer
#from app.utils import CONFIG, ARCHIVE_ROOT
#from pathlib import Path
from app.presentation.new_sermon import render_new_sermon




def new():
    """Skapa en ny predikan"""
    print('Skapa en ny predikan')
    title = typer.prompt('Titel')
    context = typer.prompt('Sammanhang')
    print(f"title: {title}, context: {context}")
