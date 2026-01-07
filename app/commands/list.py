import typer

app = typer.Typer()

@app.command()
def all():
    """Lista alla predikningar"""
    print("Listar alla predikningar")

@app.command()
def recent():
    """Lista senaste predikningar"""
    print("Listar senaste")



