import typer
from app.presentation.common import clear_screen
from app.services.podcast import publish_episode, prune_podcast, list_episodes


app = typer.Typer(help = 'Hantera podcast för predikningar och externt material', no_args_is_help=True)


@app.command()
def publish(sermon_code: str):
    """Publicera ett podcastavsnitt med en exporterad predikan eller extern fil."""
    print(f"Exportera predikan {sermon_code} som podcast.")
    publish_episode(sermon_code)
    # Equivalent commands for publishing sermon in database:
    #   sermon export podcast P382
    #   sermon podcast publish P382
    # This command also publishes other files:
    #   sermon podcast publish andakt.mp3


@app.command()
def prune():
    """Rensar gamla avsnitt från podcasten."""
    prune_podcast()


@app.command()
def list():
    """Få en överblick över tillgängliga avsnitt."""
    list_episodes()


@app.command()
def remove():
    """Radera ett avsnitt i podcasten."""
    pass


@app.command()
def update():
    """Uppdatera ett avsnitt i podcasten."""
    pass




