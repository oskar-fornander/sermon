
import typer

app = typer.Typer(help = "Koppla bibelreferens(er), gudstjänst, manuskript, inspelning eller övrig resurs till en predikan")

@app.command()
def service(sermon_id: str, date: str, place: str, notice: str = typer.Option('', '--notice', '-n')):
    """Koppla en gudstjänst till predikan"""
    print(f"Koppla en gudstjänst till predikan {sermon_id}")

@app.command()
def manuscript(sermon_id: str, file_name: str):
    """Koppla ett manuskript till predikan"""
    print(f"Koppla ett manuskript till predikan {sermon_id}")

@app.command()
def recording(sermon_id: str, date: str, media_type: str, file_name: str):
    """Koppla en inspelning till predikan"""
    print(f"Koppla en inspelning till predikan {sermon_id}")

@app.command()
def resource(sermon_id: str, file_name: str):
    """Koppla en övrig resurs till predikan"""
    print(f"Koppla en övrig resurs till predikan {sermon_id}")

@app.command()
def bible_reference(sermon_id: str, reference: str):
    """Koppla en eller flera bibelreferenser till predikan"""
    print(f"Koppla en eller flera bibelreferenser till predikan {sermon_id} (allt som en sträng, separerat med semikolon, t.ex. Joh 1:1-5; Joh 8:12; 1 Mos 1:1-3")


