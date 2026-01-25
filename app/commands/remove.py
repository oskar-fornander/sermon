
import typer
from app.presentation.common import clear_screen

app = typer.Typer(help = 'Radera bibelreferens(er), gudstjänst, manuskript, inspelning eller övrig resurs som är kopplad till en predikan')

@app.command()
def service(sermon_code: str, date: str, place: str, notice: str = typer.Option('', '--notice', '-n')):
    """Radera en gudstjänst som är kopplad till predikan"""
    print(f"Radera en gudstjänst som är kopplad till predikan {sermon_code}")

@app.command()
def manuscript(sermon_code: str, file_name: str):
    """Radera ett manuskript som är kopplat till predikan"""
    print(f"Radera ett manuskript som är kopplat till predikan {sermon_code}")

@app.command()
def recording(sermon_code: str, date: str, media_type: str, file_name: str):
    """Radera en inspelning som är kopplad till predikan"""
    print(f"Radera en inspelning som är kopplad till predikan {sermon_code}")

@app.command()
def resource(sermon_code: str, file_name: str):
    """Radera en övrig resurs som är kopplad till predikan"""
    print(f"Radera en övrig resurs som är kopplad till predikan {sermon_code}")

@app.command()
def bible_reference(sermon_code: str, reference: str):
    """Radera en eller flera bibelreferenser som är kopplade till predikan"""
    print(f"Radera en eller flera bibelreferenser som är kopplade till predikan {sermon_code} (allt som en sträng, separerat med semikolon, t.ex. Joh 1:1-5; Joh 8:12; 1 Mos 1:1-3")


