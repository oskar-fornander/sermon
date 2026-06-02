import typer
from app.presentation.common import clear_screen
from app.services.export_html import export_html
from app.services.podcast import publish_episode


app = typer.Typer(help = 'Exportera registret som html eller enskild predikan som podcast', no_args_is_help=True)


@app.command()
def html():
    """Exportera predikoregistret som html."""
    print("Exportera listan av predikningar som html")
    export_html()


@app.command()
def podcast(sermon_code: str):
    """Exportera en predikan som podcast."""
    print(f"Exportera predikan {sermon_code} som podcast.")
    publish_episode(sermon_code)

    # sermon export podcast P382

