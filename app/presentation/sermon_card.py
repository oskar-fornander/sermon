
from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from pathlib import Path
from app.presentation.common import *


def render_sermon_card(sermon, services, manuscripts, recordings, resources, bible_references, related_sermons):
    """Render a sermon card to show a sermon to the user."""


    table = Table(title=None, box=box.SIMPLE, expand=False) #A table inside the panel

    table.add_column('Kod', style='sermon_code', no_wrap=True, min_width=4)
    table.add_column('[key]Datum[/]', style='key',  width=10)
    table.add_column('Plats', no_wrap=True, min_width=4, overflow='ellipsis')
    table.add_column('Titel', no_wrap=True, min_width=4, overflow='ellipsis')




    elements = []  # Gather elements to build the panel

    notes = sermon['notes']
    report = sermon['report']
    if sermon['context']:
        elements.append(Align.right(f" [info]{sermon['context']}[/info]"))
    else:
        elements.append('')
    bible_reference_text = ', '.join([x['reference_text'] for x in bible_references])
    if bible_reference_text:
        elements.append(f"{bible_reference_text}")
    elements.append('')
    elements.append(f"[title]Introduktion:[/title] {sermon['introduction']}")
    elements.append(f"[title]Budskap:[/title] {sermon['message']}")
    if notes:
        elements.append(f"[title]Kommentar:[/title] {notes}")
    if report:
        elements.append(f"[title]Omdöme:[/title] {report}")

    body = Group(*elements)


    for service in services:
        service_txt = f"{service['date']} {service['place']}"
        if service['notes']:
            service_txt += f" ({service['notes']})"
        elements.append(service_txt)

    for manuscript in manuscripts:
        manuscript_file_path = PATH_MANUSCRIPTS / Path(manuscript['file_name'])
        manuscript_txt = f"[link=file://{manuscript_file_path}]{manuscript['file_name']}[/link] ({manuscript['date']})"
        if manuscript['notes']:
            manuscript_txt += f" ({manuscript['notes']})"
        elements.append(manuscript_txt)

    for recording in recordings:
        recording_file_path = PATH_RECORDINGS / Path(recording['file_name'])
        recording_txt = f"[link=file://{recording_file_path}]{recording['file_name']}[/link] ({recording['date']})"
        if recording['notes']:
            recording_txt += f" ({recording['notes']})"
        elements.append(recording_txt)


#PATH_RESOURCES


    console.print('[link=https://www.google.com]länk[/link]')




    #body = Group(elements)
    #body = f"test"
    title = f"[title][key]{sermon['code']}[/key] ─── {sermon['title']}[/title]"
    subtitle = f"[dim]Tips:[/] [code]sermon open manuscript {sermon['code']}[/]"
    print()
    console.print(
        Panel(body,
            title=title,
            title_align='left', 
            subtitle=subtitle,
            subtitle_align='right',
            box=box.ROUNDED 
        )
    )
    print()

#sermon:
# x code
# x title
# x context
# x introduction
# x message
# x report
# x notes

# Bible reference:
# x reference_text

#service:
# x date
# x place
# x notes

#manuscript:
#   file_name
#   version
#   date
#   notes

# recording:
#   type
#   date
#   file_name
#   external_url
#   notes

#resource:
#   file_name
#   title
#   notes

#related_sermons:
#   related_sermon_id











