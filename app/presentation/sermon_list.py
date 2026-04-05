
from app.config import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from app.utils import get_file_link
from app.presentation.common import *


def render_sermon_list(title='Predikoarkiv', content='', subtitle='', sermons=[], dates=[], order_by='code', reverse = False):
    """Render a presentation of a list of sermons, sorted by code or date."""

    if not reverse:  # Reverse for presentation?
        sermons = sermons[::-1]
        dates = dates[::-1]

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
    

    #for sermon in sermons:  
    for i, sermon in enumerate(sermons):  # Each sermon is a sermonDraft
        # Join all manuscripts, recordings and resources into single string for presentation in table
        manuscript = ' '.join([get_file_link(PATH_MANUSCRIPTS, x.file_name, title=LIST_MARKER, show_title_if_missing=False) for x in sermon.manuscripts])
        recording = ' '.join([get_file_link(PATH_RECORDINGS, x.file_name or x.external_url, title=LIST_MARKER, show_title_if_missing=False) for x in sermon.recordings])
        resource = ' '.join([get_file_link(PATH_RESOURCES, x.file_name, title=LIST_MARKER, show_title_if_missing=False) for x in sermon.resources])

        if order_by == 'date':
            date, place = '', ''
            if sermon.services:
                for s in sermon.services:  # Find the correct service to show
                    if s.date == dates[i]:
                        date = s.date  # Date of the service to show
                        place = s.place
            table.add_row(sermon.code, date, place, sermon.title, manuscript, recording, resource, sermon.report)
        else: #code
            service = ''
            if sermon.services:
                service = ', '.join([s.date for s in sermon.services][::-1]) #Show all services in descending order
            table.add_row(sermon.code, sermon.title, service, manuscript, recording, resource, sermon.report)


    if subtitle is None:
        subtitle = f""  # Subtitle for search result: ''
    elif subtitle == '':  # Default subtitle
        last_sermon = sermons[-1].code if len(sermons) > 0 else 'P000'
        subtitle = f"[tip]Tips:[/] [code]sermon show {last_sermon}[/]"

    body = Group(f"\n[info]{content}[/info]", table)
    print()
    console.print(
        Panel(body,
            title = f"[title]{title}[/title]",
            title_align = 'left', 
            subtitle = subtitle,
            subtitle_align = 'right',
            box = box.ROUNDED 
        )
    )
    #print()

