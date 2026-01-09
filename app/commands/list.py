import typer

app = typer.Typer(help = "Lista alla eller några av predikningarna.")

@app.command()
def all():
    """Lista alla predikningar"""
    print("Listar alla predikningar")

@app.command()
def recent(n: int = 5):
    """Lista senaste n predikningar"""
    print(f"Listar {n} senaste predikningarna")



