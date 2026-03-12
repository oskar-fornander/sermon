import typer
from app.errors import *
from app.presentation.common import console, clear_screen
from app.tools.files import check_files


app = typer.Typer(help = 'Hantering av filer kopplade till predikningar i databasen')


@app.command('check')
def check():
    """Kontrollera oanvända och saknade filer"""
    clear_screen()
    console.print('Kontrollerar oanvända och saknade filer')
    check_files()


@app.command('view')
def view():
    """Visa filer i finder"""
    clear_screen()
    console.print('Visa filer i finder ...')

