import typer

from app.db import CONFIG


from app.commands import list as list_commands
from app.commands import attach as attach_commands
from app.commands import export as export_commands

from app.commands.show import show
from app.commands.search import search
from app.commands.new import new
from app.commands.edit import edit


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

