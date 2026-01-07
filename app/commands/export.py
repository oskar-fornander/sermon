
import typer

app = typer.Typer()

@app.command()
def html():
    """Exportera predikoregistret som html."""
    print("Exportera listan av predikningar som html")

@app.command()
def podcast(sermon_id: str):
    """Exportera en predikan som podcast."""
    print(f"Exportera predikan {sermon_id} som podcast.")
