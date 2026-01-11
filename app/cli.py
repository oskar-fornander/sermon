import typer

from db import CONFIG

from commands import list as list_commands
from commands import attach as attach_commands
from commands import export as export_commands

from commands.show import show
from commands.search import search
from commands.new import new
from commands.edit import edit


app = typer.Typer(help = "Predikoarkiv")

#Sub commands
app.add_typer(list_commands.app, name = "list")
app.add_typer(attach_commands.app, name = "attach")
app.add_typer(export_commands.app, name = "export")

#Single commands
app.command()(show)
app.command()(search)
app.command()(new)
app.command()(edit)






from pathlib import Path
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

ARCHIVE_ROOT = Path(config["archive"]["root"]).resolve()











if __name__ == "__main__":
    app()

