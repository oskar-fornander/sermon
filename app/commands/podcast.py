import typer
from app.presentation.common import clear_screen
from app.services.podcast import upload_sermon_to_podcast


app = typer.Typer(help = 'Hantera podcast för predikningar och externt material', no_args_is_help=True)


@app.command()
def view():
    """Få en överblick över tillgängliga avsnitt."""
    print("Få en överblick över tillgängliga avsnitt.")
    pass


@app.command()
def publish():
    """Publicera ett podcastavsnitt med extern fil."""
    print("Publicera ett podcastavsnitt med extern fil.")

    pass


@app.command()
def upload(sermon_code: str):
    """Exportera en predikan som podcast."""
    print(f"Exportera predikan {sermon_code} som podcast.")
    upload_sermon_to_podcast(sermon_code)
    # Equivalent commands:
    #   sermon export podcast P382
    #   sermon podcast upload P382

