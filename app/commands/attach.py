
import typer

app = typer.Typer()

@app.command()
def service(id: str):
    """Koppla en gudstjänst till predikan"""
    print(f"Koppla en gudstjänst till predikan {id}")

@app.command()
def manuscript(id: str):
    """Koppla ett manuskript till predikan"""
    print(f"Koppla ett manuskript till predikan {id}")

@app.command()
def recording(id: str):
    """Koppla en inspelning till predikan"""
    print(f"Koppla en inspelning till predikan {id}")

@app.command()
def resource(id: str):
    """Koppla en övrig resurs till predikan"""
    print(f"Koppla en övrig resurs till predikan {id}")

