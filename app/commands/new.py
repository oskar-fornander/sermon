
import typer


def new():
    """Skapa en ny predikan"""
    print("Skapa en ny predikan")
    title = typer.prompt("Titel")
    context = typer.prompt("Sammanhang")
