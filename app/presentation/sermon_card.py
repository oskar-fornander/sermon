from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from pathlib import Path
from app.presentation.common import *


def render_sermon_card(sermon, services, manuscripts, recordings, resources, bible_references, related_sermons):
    """Render a sermon card to show a sermon to the user."""

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
    elements.append(f"[title]Introduktion:[/title] {sermon['introduction'] or '–'}")
    elements.append(f"[title]Budskap:[/title] {sermon['message'] or '–'}")
    if notes:
        elements.append(f"[title]Kommentar:[/title] {notes}")
    #if report:
    elements.append(f"[title]Omdöme:[/title] {report or '–'}")
    if related_sermons:
        related_sermons = ', '.join([r['code'] for r in related_sermons])
        elements.append(f"[title]Relaterad predikan:[/title] {related_sermons}")


    # Add services
    elements.append('[title]Gudstjänst:[/]')
    if not services:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for service in services:
        elements.append(f"{TAB}{service['date']}  {service['place']}")
        if service['notes']:
            elements[-1] += f"{TAB}[notes]• {service['notes']}[/notes]"  # Add notes at end of the same line

    # Add manuscripts
    elements.append('[title]Manus:[/]')
    if not manuscripts:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for manuscript in manuscripts:
        manuscript_file_path = PATH_MANUSCRIPTS / Path(manuscript['file_name'])
        elements.append(f"{TAB}[notes]{manuscript['date']}[/notes]  [link=file://{manuscript_file_path}]{manuscript['file_name']}[/link]")
        if manuscript['notes']:
            elements[-1] += f"{TAB}[notes]• {manuscript['notes']}[/notes]"  # Add notes at end of the same line
            #elements.append(f"{TAB + ' ' * 12}[notes]• {manuscript['notes']}[/notes]")

    # Add recordings
    elements.append('[title]Inspelning:[/]')
    if not recordings:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for recording in recordings:
        if recording['file_name']:
            recording_file_path = PATH_RECORDINGS / Path(recording['file_name'])
            elements.append(f"{TAB}[notes]{recording['date']}[/notes]  [link=file://{recording_file_path}]{recording['file_name']}[/link]  [notes]{recording['type']}[/notes]")
        elif recording['external_url']: # Either a local file OR an external link for each recording
            link_title = 'extern url'
            elements.append(f"{TAB}[notes]{recording['date']}[/notes]  [link={recording['external_url']}]{link_title}[/link]  [notes]{recording['type']}[/notes]")
        if recording['notes']:
            elements[-1] += f"{TAB}[notes]• {recording['notes']}[/notes]"  # Add notes at end of the same line

    # Add resources
    elements.append('[title]Resurs:[/]')
    if not resources:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for resource in resources:
        resource_file_path = PATH_RESOURCES / Path(resource['file_name'])
        elements.append(f"{TAB}[notes]{resource['date']}[/notes]  [link=file://{resource_file_path}]{resource['file_name']}[/link]")
        if resource['notes']:
            elements[-1] += f"{TAB}[notes]• {resource['notes']}[/notes]"  # Add notes at end of the same line


    body = Group(*elements)
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
# x file_name
#   (version)
# x date
# x notes

# recording:
# x type
# x date
# x file_name
# x external_url
# x notes

#resource:
# x file_name
# x title
# x notes

#related_sermons:
# x related_sermon_id



