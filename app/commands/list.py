import typer
from app.db import list_sermons, get_services_for_sermon


app = typer.Typer(help = 'Lista de senaste predikningarna', invoke_without_command=True)
#   sermon list [--limit N] [--all] [--date]

@app.callback()
def sermon_listing_function(
        limit: int = typer.Option(3, '--limit', '-n', help='Antal predikningar att visa'),
        all: bool = typer.Option(False, '--all', help='Visa alla predikningar'), 
        date: bool = typer.Option(False, '--date', help='Sorterat efter datum för framförande istället för kod'),
        reverse: bool = typer.Option(False, '--reverse', '-r', help='Omvänd sortering')
        ):
    """Lista alla eller några av predikningarna"""
    print('Listar predikningar')
    
    sermons = []
    if date:
        sermons = list_sermons('date') #List sermons by service dates
    else: #code
        sermons = list_sermons('code') #List sermons by code, e.g. P372

    if not all: #Show all sermons if the flag --all is set, otherwise
        sermons = sermons[-limit:] #crop the list to only include the number of sermons desired by the flag --limit/-n
    if reverse:
        sermons.reverse() #Reverse the sorted list if flag --reverse is set

    for sermon in sermons:
        if date:
            txt = f"{sermon['code']} {sermon['date']} {sermon['place']} {sermon['title']}"
            print(txt)
        else: #code
            services = get_services_for_sermon(sermon['code'])
            service = ''
            if len(services) > 0:
                service = services[-1]['date'] #Show only last service
                service = ', '.join([s['date'] for s in services][::-1]) #Show all services in descending order
            print(f"{sermon['code']} {sermon['title']} {service}")

