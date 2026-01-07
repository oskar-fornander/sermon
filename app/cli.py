import typer
from commands import list as list_commands

app = typer.Typer(help = "Predikoarkiv")
app.add_typer(list_commands.app, name = "list")



if __name__ == "__main__":
    app()

