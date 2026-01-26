from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from app.presentation.common import *
from app.utils import get_file_link


def render_sermon_card(sermon_draft, preview=False):
    """Render a sermon card to show a sermon to the user. Also used to preview a draft."""

    elements = []  # Gather elements to build the panel

    notes = sermon_draft.notes
    report = sermon_draft.report
    if sermon_draft.context:
        elements.append(Align.right(f" [info]{sermon_draft.context}[/info]"))
    else:
        elements.append('')
    bible_reference_text = '; '.join(sermon_draft.bible_references)
    if bible_reference_text:
        elements.append(f"{bible_reference_text}")
    elements.append('')
    elements.append(f"[title]Introduktion:[/title] {sermon_draft.introduction or '–'}")
    elements.append(f"[title]Budskap:[/title] {sermon_draft.message or '–'}")
    if notes:
        elements.append(f"[title]Kommentar:[/title] {notes}")
    #if report:
    elements.append(f"[title]Omdöme:[/title] {report or '–'}")
    related_sermons = sermon_draft.related_sermons
    if related_sermons:
        related_sermons = ', '.join([r['code'] for r in related_sermons])
        elements.append(f"[title]Relaterad predikan:[/title] {related_sermons}")


    # Add services
    elements.append('[title]Gudstjänst:[/]')
    services = sermon_draft.services
    if not services:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for service in services:
        elements.append(f"{TAB}{service.date}  {service.place}")
        if service.notes:
            elements[-1] += f"{TAB}[notes]• {service.notes}[/notes]"  # Add notes at end of the same line

    # Add manuscripts
    elements.append('[title]Manus:[/]')
    manuscripts = sermon_draft.manuscripts
    if not manuscripts:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for manuscript in manuscripts:
        link = get_file_link(PATH_MANUSCRIPTS, manuscript.file_name)
        elements.append(f"{TAB}[notes]{manuscript.date}[/notes]  {link}")
        if manuscript.notes:
            elements[-1] += f"{TAB}[notes]• {manuscript.notes}[/notes]"  # Add notes at end of the same line
            #elements.append(f"{TAB + ' ' * 12}[notes]• {manuscript['notes']}[/notes]")

    # Add recordings
    recordings = sermon_draft.recordings
    elements.append('[title]Inspelning:[/]')
    if not recordings:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for recording in recordings:
        if recording.file_name:
            link = get_file_link(PATH_RECORDINGS, recording.file_name)
            elements.append(f"{TAB}[notes]{recording.date}[/notes]  {link}")
        elif recording.external_url: # Either a local file OR an external link for each recording
            link_title = 'extern url'
            elements.append(f"{TAB}[notes]{recording.date}[/notes]  [link={recording.external_url}]{link_title}[/link]  [notes]{recording.type}[/notes]")
        if recording.notes:
            elements[-1] += f"{TAB}[notes]• {recording.notes}[/notes]"  # Add notes at end of the same line

    # Add resources
    resources = sermon_draft.resources
    elements.append('[title]Resurs:[/]')
    if not resources:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for resource in resources:
        resource_title = resource.title or resource.file_name  # Use file name if no title exists
        link = get_file_link(PATH_RESOURCES, resource.file_name, title=resource_title)
        elements.append(f"{TAB + 12 * ' '}{link}")
        if resource.notes:
            elements[-1] += f"{TAB}[notes]• {resource.notes}[/notes]"  # Add notes at end of the same line


    body = Group(*elements)
    title = f"[title][key]{sermon_draft.code}[/key] ─── {sermon_draft.title}[/title]"
    subtitle = f"[dim]Tips:[/] [code]sermon open manuscript {sermon_draft.code}[/]"
    style = ''
    if preview:  # Other title and subtitle if it is a preview that is shown
        title = f"[title]FÖRHANDSGRANSKNING: [key]{sermon_draft.code}[/key] ─── {sermon_draft.title}[/title]"
        subtitle = f"[dim]Tips:[/] Lägg till fler resurser i efterhand med t.ex. [code]sermon add recording[/]"
        style = 'on gray15'

    print()
    console.print(
        Panel(body,
            title=title,
            title_align='left', 
            subtitle=subtitle,
            subtitle_align='right',
            box=box.ROUNDED,
            style=style
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



