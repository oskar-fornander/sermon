import typer

app = typer.Typer(help = "Lista alla eller några av predikningarna.")

#(limit: int = typer.Option(10, '--limit', '-n'), all: str = typer.Option('all', '--all', '-a'), sort: str = typer.Option('code', '--sort', '-s'), reversed: bool = typer.Option(False, '--reversed', '-r')):





# Update list function. Syntax:

#   sermon list [--limit N] [--sort FIELD] [--reversed True]

#Need to rewrite the two functions below to a single and interpret the options.
#Add option like [code | date | title] etc?




@app.command()
def all():
    """Lista alla predikningar"""
    print("Listar alla predikningar")

@app.command()
def recent(n: int = 5):
    """Lista senaste n predikningar"""
    print(f"Listar {n} senaste predikningarna")



