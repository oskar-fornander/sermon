
from app.config import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from app.utils import get_file_link
from app.presentation.common import *


def render_sermon_list(title='', sermons=[], order_by='code', reverse = False):
    """Render a presentation of a list of sermons, sorted by code or date."""

    if not reverse:  # Reverse for presentation?
        sermons.reverse()

    table = Table(title=None, box=box.SIMPLE, expand=False, row_styles=['', 'on black']) #A table inside the panel

    if order_by == 'date': #Set headers based on ordered by code or date
        table.add_column('Kod', style='sermon_code', no_wrap=True, min_width=4)
        table.add_column('[key]Datum[/]', style='key', width=14, overflow='ellipsis')
        table.add_column('Plats', no_wrap=True, min_width=4, max_width=30, overflow='ellipsis')
        table.add_column('Titel', no_wrap=True, min_width=4, overflow='ellipsis')
    else:
        table.add_column('[key]Kod[/]', style='key', no_wrap=True, min_width=4)
        table.add_column('Titel', no_wrap=True, min_width=4, max_width=40, overflow='ellipsis')
        table.add_column('Datum',  min_width=10, no_wrap=True, width=12, overflow='ellipsis')
        #Setting min_width, no_wrap and overflow does not seem to work properly
    table.add_column(ICON['manuscript'], no_wrap=True) # table.add_column('Manus')
    table.add_column(ICON['recording'], no_wrap=True) # table.add_column('Inspelning')
    table.add_column(ICON['resource'], no_wrap=True) # table.add_column('Resurs')
    table.add_column('±', style='notes', no_wrap=True)  # Report column
    

    for sermon in sermons:  # Each sermon is a sermonDraft

        # Join all manuscripts, recordings and resources into single string for presentation in table
        #manuscript = ' '.join([f"[link=file://{PATH_MANUSCRIPTS}/{x.file_name}][link_style]{LIST_MARKER}[/]" for x in sermon.manuscripts])
        #recording = ' '.join([f"[link=file://{PATH_RECORDINGS}/{x.file_name}][link_style]{LIST_MARKER}[/]" for x in sermon.recordings])
        #resource = ' '.join([f"[link=file://{PATH_RESOURCES}/{x.file_name}][link_style]{LIST_MARKER}[/]" for x in sermon.resources])
        manuscript = ' '.join([get_file_link(PATH_MANUSCRIPTS, x.file_name, title=LIST_MARKER, show_title_if_missing=False) for x in sermon.manuscripts])
        recording = ' '.join([get_file_link(PATH_RECORDINGS, x.file_name or x.external_url, title=LIST_MARKER, show_title_if_missing=False) for x in sermon.recordings])
        resource = ' '.join([get_file_link(PATH_RESOURCES, x.file_name, title=LIST_MARKER, show_title_if_missing=False) for x in sermon.resources])


        if order_by == 'date':
            if sermon.services:
                date = sermon.services[-1].date  # Get the last date this sermon was preached in a service
                place = sermon.services[-1].place
                table.add_row(sermon.code, date, place, sermon.title, manuscript, recording, resource, sermon.report)
        else: #code
            service = ''
            if sermon.services:
                service = ', '.join([s.date for s in sermon.services][::-1]) #Show all services in descending order
            table.add_row(sermon.code, sermon.title, service, manuscript, recording, resource, sermon.report)


    body = Group(f"[info]{title}[/info]", table)
    last_sermon = sermons[-1].code if len(sermons) > 0 else 'P000'
    print()
    console.print(
        Panel(body,
            title = f"[title]Predikoarkiv[/title]",
            title_align = 'left', 
            subtitle = f"[tip]Tips:[/] [code]sermon show {last_sermon}[/]",
            subtitle_align = 'right',
            box = box.ROUNDED 
        )
    )
    print()

