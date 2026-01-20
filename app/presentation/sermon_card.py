
from app.utils import CONFIG, ARCHIVE_ROOT, PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from pathlib import Path
from app.presentation.common import *






def render_sermon_card(sermon, services, manuscripts, recordings, resources, bible_references, related_sermons):
    """Render a sermon card to show a sermon to the user."""



    table = Table(title='Inspelningar')
    table.add_column('Typ')
    table.add_column('Datum')
    table.add_column('Fil')
    table.add_row('MP3', '2024-06-09', 'p370.mp3')
    table.add_row('Video', '2024-06-09', 'länk')
    console.print(table)

    
    body = (
        '[bold]Plats:[/bold] Storkyrkan\n'
        '[bold]Text:[/bold] Joh 3:16\n'
        '[bold]Betyg:[/bold] A\n\n'
        'Här kan själva predikotexten eller sammanfattningen visas.'
    )
    console.print(Panel(Columns([body, table]), title='P370 – Nådens evangelium'))

    color = Color.from_rgb(100, 100, 100)
    color = Color.default()
    bgcolor = Color.from_rgb(0, 0, 0)
    bgcolor = Color.default()
    my_style = Style(color = Color.from_rgb(255, 0, 0), bold = True)
    title = f"[bold]{sermon['code']}[/bold] ─── {sermon['title']}"
    subtitle = 'Oskar Fornander'

    notes = sermon['notes']
    report = sermon['report']
    elements = []
    if sermon['context']:
        elements.append(Align.right(f" [italic]{sermon['context']}[/italic]"))
    else:
        elements.append('')
    bible_reference_text = ', '.join([x['reference_text'] for x in bible_references])
    if bible_reference_text:
        elements.append(f"{bible_reference_text}")
    elements.append("")
    elements.append(f"[bold]Introduktion:[/bold] {sermon['introduction']}")
    elements.append(f"[bold]Budskap:[/bold] {sermon['message']}")
    if notes:
        elements.append(f"[bold]Kommentar:[/bold] {notes}")
    if report:
        elements.append(f"[bold]Omdöme:[/bold] {report}")

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


    console.print('[link=https://www.google.com]https://www.google.com[/link]')
    console.print('[link=https://www.google.com]länk[/link]')
    console.print('länk', style = 'link https://www.google.com')






    body = Group(*elements)
    console.print(
        Panel(body,
            title = title,
            title_align = 'left', 
            subtitle = subtitle,
            subtitle_align = 'right',
            box = box.ROUNDED 
        )
    )
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











