
import typer

app = typer.Typer(help = "Koppla bibelreferens(er), gudstjänst, manuskript, inspelning eller övrig resurs till en predikan")

@app.command()
def service(sermon_code: str, date: str, place: str, notice: str = typer.Option('', '--notice', '-n')):
    """Koppla en gudstjänst till predikan"""
    print(f"Koppla en gudstjänst till predikan {sermon_code}")

@app.command()
def manuscript(sermon_code: str, file_name: str):
    """Koppla ett manuskript till predikan"""
    print(f"Koppla ett manuskript till predikan {sermon_code}")

@app.command()
def recording(sermon_code: str, date: str, media_type: str, file_name: str):
    """Koppla en inspelning till predikan"""
    print(f"Koppla en inspelning till predikan {sermon_code}")

@app.command()
def resource(sermon_code: str, file_name: str):
    """Koppla en övrig resurs till predikan"""
    print(f"Koppla en övrig resurs till predikan {sermon_code}")

@app.command()
def bible_reference(sermon_code: str, reference: str):
    """Koppla en eller flera bibelreferenser till predikan"""
    print(f"Koppla en eller flera bibelreferenser till predikan {sermon_code} (allt som en sträng, separerat med semikolon, t.ex. Joh 1:1-5; Joh 8:12; 1 Mos 1:1-3")


