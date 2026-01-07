
import typer

app = typer.Typer()

@app.command()
def all():
    """Hantera gudstjänst kopplad till predikan"""
    print("Hantera gudstjänst")

