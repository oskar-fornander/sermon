
from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from app.presentation.common import *


def render_sermon_list(title, sermons, services = None, manuscripts = None, recordings = None, resources = None, order_by = 'code'):
    """Render a presentation of a list of sermons, sorted by code or date."""

    table = Table(title=None, box=box.SIMPLE, expand=False) #A table inside the panel

    if order_by == 'date': #Set headers based on ordered by code or date
        table.add_column('Kod', style='sermon_code', no_wrap=True, min_width=4)
        table.add_column('[key]Datum[/]', style='key',  width=10)
        table.add_column('Plats', no_wrap=True, min_width=4, overflow='ellipsis')
        table.add_column('Titel', no_wrap=True, min_width=4, overflow='ellipsis')
    else:
        table.add_column('[key]Kod[/]', style='key', no_wrap=True)
        table.add_column('Titel', no_wrap=True, min_width=4, overflow='ellipsis')
        table.add_column('Datum',  min_width=10, no_wrap=True)
        #Setting min_width, no_wrap and overflow does not seem to work properly
    table.add_column(ICON['manuscript']) # table.add_column('Utkast')
    table.add_column(ICON['recording']) # table.add_column('Inspelning')
    table.add_column(ICON['resource']) # table.add_column('Resurs')
    

    for i in range(len(sermons)):
        sermon = sermons[i]

        # Join all manuscripts, recordings and resources into single string for presentation in table
        manuscript = ' '.join([f"[link=file://{PATH_MANUSCRIPTS}/{x['file_name']}][link_style]+[/]" for x in manuscripts[i]])
        recording = ' '.join([f"[link=file://{PATH_RECORDINGS}/{x['file_name']}][link_style]+[/]" for x in recordings[i]])
        resource = ' '.join([f"[link=file://{PATH_RESOURCES}/{x['file_name']}][link_style]+[/]" for x in resources[i]])

        if order_by == 'date':
            table.add_row(sermon['code'], sermon['date'], sermon['place'], sermon['title'], manuscript, recording, resource)
        else: #code
            service = ''
            if services and services[i]:
                service = ', '.join([s['date'] for s in services[i]][::-1]) #Show all services in descending order
            table.add_row(sermon['code'], sermon['title'], service, manuscript, recording, resource)

    console.print('[link=https://www.google.com]länk[/link]')
    console.print('länk', style = 'link https://www.google.com')

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

