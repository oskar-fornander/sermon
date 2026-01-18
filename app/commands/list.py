import typer


app = typer.Typer(help = "Lista de senaste predikningarna", invoke_without_command=True)
#   sermon list [--limit N] [--all] [--date]

@app.callback()
def list_sermons(
        limit: int = typer.Option(10, '--limit', '-n', help='Antal predikningar att visa'),
        all: bool = typer.Option(False, '--all', help='Visa alla predikningar'), 
        date: bool = typer.Option(False, '--date', help='Sorterat efter datum för framförande istället för kod')
        ):
    """Lista alla eller några av predikningarna"""
    print("Listar predikningar")

