import typer

from commands import list as list_commands
from commands import service as service_commands
from commands import export as export_commands

from commands.show import show
from commands.search import search
from commands.new import new
from commands.edit import edit


app = typer.Typer(help = "Predikoarkiv")

#Sub commands
app.add_typer(list_commands.app, name = "list")
app.add_typer(service_commands.app, name = "service")
app.add_typer(export_commands.app, name = "export")

#Single commands
app.command()(show)
app.command()(search)
app.command()(new)
app.command()(edit)


if __name__ == "__main__":
    app()

