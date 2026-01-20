import typer
from app.db import list_sermons, get_services_for_sermon, get_manuscripts_for_sermon, get_recordings_for_sermon, get_resources_for_sermon
from app.presentation.sermon_list import render_sermon_list


app = typer.Typer(help = 'Lista de senaste predikningarna', invoke_without_command=True)
#   sermon list [--limit N] [--all] [--date] [--reverse]

@app.callback()
def sermon_listing_function(
        limit: int = typer.Option(3, '--limit', '-n', help='Antal predikningar att visa'),
        all: bool = typer.Option(False, '--all', help='Visa alla predikningar'), 
        date: bool = typer.Option(False, '--date', help='Sorterat efter datum för framförande istället för kod'),
        reverse: bool = typer.Option(False, '--reverse', '-r', help='Omvänd sortering')):
    """Lista alla eller några av predikningarna"""
    
    sermons = []
    if date:
        sermons = list_sermons('date') #List sermons by service dates
    else: #code
        sermons = list_sermons('code') #List sermons by code, e.g. P372

    n = 'Alla predikningar listade'
    if not all: #Show all sermons if the flag --all is set, otherwise
        sermons = sermons[-limit:] #crop the list to only include the number of sermons desired by the flag --limit/-n
        n = f"De {min(limit, len(sermons))} senaste predikningarna listade"

    if reverse:
        sermons.reverse() #Reverse the sorted list if flag --reverse is set


    manuscripts = [get_manuscripts_for_sermon(sermon['code']) for sermon in sermons] #Get all manuscripts for each sermon and store in a list
    recordings = [get_recordings_for_sermon(sermon['code']) for sermon in sermons] 
    resources = [get_resources_for_sermon(sermon['code']) for sermon in sermons] 

    if date:
        title = f" {n} efter predikodatum"
        render_sermon_list(title=title, sermons=sermons, manuscripts=manuscripts, recordings=recordings, resources=resources, order_by='date')
    else:
        title = f" {n} efter predikokod"
        services = [get_services_for_sermon(sermon['code']) for sermon in sermons] #Get all services for each sermon and store in a list
        render_sermon_list(title=title, sermons=sermons, services=services, manuscripts=manuscripts, recordings=recordings, resources=resources, order_by='code')


