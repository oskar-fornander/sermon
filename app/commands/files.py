import typer
import subprocess
from app.errors import *
from app.presentation.common import console, clear_screen
from app.tools.files import check_files
from app.config import PATH_MANUSCRIPTS


app = typer.Typer(help = 'Hantering av filer kopplade till predikningar i databasen', no_args_is_help=True)


@app.command('check')
def check():
    """Kontrollera oanvända och saknade filer"""
    clear_screen()
    console.print('Kontrollerar oanvända och saknade filer')
    check_files()


@app.command('view')
def view():
    """Visa filer i finder"""
    #clear_screen()
    console.print('Visar filer i finder')
    subprocess.run(['open', str(PATH_MANUSCRIPTS.parent)])



