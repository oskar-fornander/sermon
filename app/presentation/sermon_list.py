
from app.presentation.common import *


def render_sermon_list(title, sermons, services = None, order_by = 'code'):
    """Render a presentation of a list of sermons, sorted by code or date."""

    table = Table(title=None, box=box.SIMPLE, expand=False) #A table inside the panel

    if order_by == 'date': #Set headers based on ordered by code or date
        table.add_column('Kod', style='sermon_code', no_wrap=True, min_width=4)
        table.add_column('Datum', style='key',  width=10)
        table.add_column('Plats', no_wrap=True, min_width=4, overflow='ellipsis')
        table.add_column('Titel', no_wrap=True, min_width=4, overflow='ellipsis')
    else:
        table.add_column('Kod', style='key', no_wrap=True)
        table.add_column('Titel', no_wrap=True, min_width=4, overflow='ellipsis')
        table.add_column('Datum',  min_width=10, no_wrap=True)
        #Setting min_width, no_wrap and overflow does not seem to work properly
    
    for i in range(len(sermons)):
        sermon = sermons[i]
        if order_by == 'date':
            table.add_row(sermon['code'], sermon['date'], sermon['place'], sermon['title'])
        else: #code
            service = ''
            if services and services[i]:
                service = ', '.join([s['date'] for s in services[i]][::-1]) #Show all services in descending order
            table.add_row(sermon['code'], sermon['title'], service)

    body = Group(f"[info]{title}[/info]", table)
    print()
    console.print(
        Panel(body,
            title = f"[title]Predikoarkiv[/title]",
            title_align = 'left', 
            subtitle = f"[dim]Tips:[/] [code]sermon show {sermons[-1]['code']}[/]",
            subtitle_align = 'right',
            box = box.ROUNDED 
        )
    )
    print()

