import typer
from app.services.open import open_manuscript, open_recording, open_resource

#sermon open manuscript P378

app = typer.Typer(help = 'Öppna manuskript, inspelning eller resurs för en predikan', no_args_is_help=True)


@app.command('manuscript')
def _open_manuscript(sermon_code: str):
    """Öppna manus till predikan"""
    open_manuscript(sermon_code)


@app.command('recording')
def _open_recording(sermon_code: str):
    """Öppna inspelning till predikan"""
    open_recording(sermon_code)


@app.command('resource')
def _open_resource(sermon_code: str):
    """Öppna resurs till predikan"""
    open_resource(sermon_code)


