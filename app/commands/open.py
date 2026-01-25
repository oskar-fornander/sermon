import typer
from app.presentation.common import clear_screen

app = typer.Typer(help = 'Öppna manuskript, inspelning eller resurs till en predikan.')


@app.command('manuscript')
def open_manuscript(sermon_code: str):
    """Öppna manuskript till predikan"""
    print(f"Öppna manuscript till predikan {sermon_code}")


@app.command('recording')
def open_recording(sermon_code: str):
    """Öppna inspelning till predikan"""
    print(f"Öppna inspelning till predikan {sermon_code}")


@app.command('resource')
def open_resource(sermon_code: str):
    """Öppna resurs till predikan"""
    print(f"Öppna resurs till predikan {sermon_code}")


