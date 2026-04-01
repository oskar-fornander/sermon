import re
import app.config as config
from app.presentation.common import *
from app.utils import get_file_link, get_audio_length, get_pdf_pages


def render_sermon_card(sermon_draft, preview=False, menu=[], edited_fields=[], query=[]):
    """Render a sermon card to show a sermon to the user. Also used to preview a draft and show edited fields as well as highlight search results."""

    edited, edited_ = {}, {}  # Style edited fields (used when showing a preview)
    for field in edited_fields:
        edited[field] = '[edited]'  # Use this below to get styling when needed: {edited.get('context', '')}
        edited_[field] = '[/edited]'

    elements = []  # Gather elements to build the panel

    def get_menu_index(title):  # Menu index for editing
        # In preview mode (for interactive editing): show index number for each title as a menu: (4) Bibelreferenser
        if not (preview and menu):
            return ''
        i = menu.index(title) + 1
        if i < 10:
            return f"[key] {i}.[/key] "
        return f"[key]{i}.[/key] "
    TAB_ = 2 * TAB if preview else TAB  # Extra long indent for preview to fit menu numbers


    # Data or -
    sermon_title = sermon_draft.title or '-'
    context = sermon_draft.context or '-'
    bible_reference_text = '; '.join(sermon_draft.bible_references) or '-'
    introduction = sermon_draft.introduction or '-'
    message = sermon_draft.message or '-'
    notes = sermon_draft.notes or '-'
    report = sermon_draft.report or '-'
    related_sermons = ', '.join(sermon_draft.related_sermons) or '-'  # show list as a string

    # Highlight search result
    if query:
        for q in query:
            sermon_title = highlight_search_hits(sermon_title, q)
            context = highlight_search_hits(context, q)
            notes = highlight_search_hits(notes, q)
            bible_reference_text = highlight_search_hits(bible_reference_text, q)
            introduction = highlight_search_hits(introduction , q)
            message = highlight_search_hits(message, q)

    elements.append('')
    elements.append(f"[title]{get_menu_index('Sammanhang')}{edited.get('context', '')}Sammanhang:{edited_.get('context', '')}[/title] {context}")
    elements.append(f"[title]{get_menu_index('Bibelreferenser')}{edited.get('bible_references', '')}Bibelreferenser:{edited_.get('bible_references', '')}[/title] {bible_reference_text}")
    elements.append(f"[title]{get_menu_index('Introduktion')}{edited.get('introduction', '')}Introduktion:{edited_.get('introduction', '')}[/title] ")
    elements.append(Padding(f"{introduction}", (0, 0, 0, len(TAB_))))  # Indent the longer texts on their own lines
    elements.append(f"[title]{get_menu_index('Budskap')}{edited.get('message', '')}Budskap:{edited_.get('message', '')}[/title] ")
    elements.append(Padding(f"{message}", (0, 0, 0, len(TAB_))))
    elements.append(f"[title]{get_menu_index('Kommentar')}{edited.get('notes', '')}Kommentar:{edited_.get('notes', '')}[/title] {notes}")
    elements.append(f"[title]{get_menu_index('Omdöme')}{edited.get('report', '')}Omdöme:{edited_.get('report', '')}[/title] {report}")
    elements.append(f"[title]{get_menu_index('Relaterad predikan')}{edited.get('related_sermons', '')}Relaterad predikan:{edited_.get('related_sermons', '')}[/title] {related_sermons}")

    # Add services
    elements.append(f"[title]{get_menu_index('Gudstjänst')}{edited.get('services', '')}Gudstjänst:[/]")
    services = sermon_draft.services
    if not services:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for service in services:
        elements.append(f"{TAB_}{service.date}  {service.place}")
        if service.notes:
            service_notes = service.notes
            if query:  # Highlight search result
                for q in query:
                    service_notes = highlight_search_hits(service_notes, q)
            elements[-1] += f"{TAB_}[notes]• {service_notes}[/notes]"  # Add notes at end of the same line

    # Add manuscripts
    elements.append(f"[title]{get_menu_index('Manus')}{edited.get('manuscripts', '')}Manus:[/]")
    manuscripts = sermon_draft.manuscripts
    if not manuscripts:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for manuscript in manuscripts:
        link = get_file_link(config.PATH_MANUSCRIPTS, manuscript.file_name, show_meta = True)
        elements.append(f"{TAB_}[notes]{manuscript.date}[/notes]  {link}")
        if manuscript.notes:
            manuscript_notes = manuscript.notes
            if query:  # Highlight search result
                for q in query:
                    manuscript_notes = highlight_search_hits(manuscript_notes, q)
            elements[-1] += f"{TAB_}[notes]• {manuscript_notes}[/notes]"  # Add notes at end of the same line
            #elements.append(f"{TAB_ + ' ' * 12}[notes]• {manuscript['notes']}[/notes]")

    # Add recordings
    recordings = sermon_draft.recordings
    elements.append(f"[title]{get_menu_index('Inspelning')}{edited.get('recordings', '')}Inspelning:[/]")
    if not recordings:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for recording in recordings:
        if recording.file_name:
            link = get_file_link(config.PATH_RECORDINGS, recording.file_name, show_meta = True)
            elements.append(f"{TAB_}[notes]{recording.date}[/notes]  {link}")
        elif recording.external_url: # Either a local file OR an external link for each recording
            link_title = 'extern url'
            elements.append(f"{TAB_}[notes]{recording.date}[/notes]  [link={recording.external_url}]{link_title}[/link]  [notes]{recording.type}[/notes]")
        if recording.notes:
            recording_notes = recording.notes
            if query:  # Highlight search result
                for q in query:
                    recording_notes = highlight_search_hits(recording_notes, q)
            elements[-1] += f"{TAB_}[notes]• {recording_notes}[/notes]"  # Add notes at end of the same line

    # Add resources
    resources = sermon_draft.resources
    elements.append(f"[title]{get_menu_index('Resurs')}{edited.get('resources', '')}Resurs:[/]")
    if not resources:
        elements[-1] += ' – '  # Add at end of line if no data to show
    for resource in resources:
        resource_title = resource.title or resource.file_name  # Use file name if no title exists
        link = get_file_link(config.PATH_RESOURCES, resource.file_name, title=resource_title)
        elements.append(f"{TAB_ + 12 * ' '}{link}")
        if resource.notes:
            resource_notes = resource.notes
            if query:  # Highlight search result
                for q in query:
                    resource_notes = highlight_search_hits(resource_notes, q)
            elements[-1] += f"{TAB_}[notes]• {resource_notes}[/notes]"  # Add notes at end of the same line


    body = Group(*elements)
    title = f"[title][key]{sermon_draft.code}[/key] ─── {sermon_title}[/title]"
    subtitle = f"[tip]Tips:[/] [code]sermon --help[/]"
    style = ''
    if preview:  # Other title and subtitle if it is a preview that is shown
        title = f"[title][reverse] FÖRHANDSGRANSKNING [/reverse] {get_menu_index('Predikokod')}[key]{edited.get('code', '')}{sermon_draft.code}{edited_.get('code', '')}[/key] ─── {get_menu_index('Rubrik')}{edited.get('title', '')}{sermon_draft.title}{edited_.get('title', '')}[/title]"
        subtitle = f"[tip]Tips:[/] [code]sermon --help[/]"
        #style = 'on gray15'

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



def highlight_search_hits(txt, q):
    """Replace all search hits 'q' in txt with '[highlight]q[/highlight]' (case insensitive)"""
    q = q.lower()
    indices = []
    i = txt.lower().find(q)
    while i != -1:
        indices.append(i)
        i = txt.lower().find(q, i + 1)
    for i in indices[::-1]:
        txt = f"{txt[:i]}[highlight]{txt[i:i + len(q)]}[/highlight]{txt[i + len(q):]}"
    return txt


