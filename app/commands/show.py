import typer
from app.utils import CONFIG, ARCHIVE_ROOT
from pathlib import Path

import shutil
from rich.console import Console
from rich.panel import Panel #https://rich.readthedocs.io/en/stable/reference/panel.html
from rich.text import Text
from rich.console import Group
from rich.align import Align
from rich.style import Style
from rich.table import Table
from rich.columns import Columns
from rich import box
from rich.color import Color


from app.db import (
    get_sermon_by_code,
    get_services_for_sermon,
    get_manuscripts_for_sermon,
    get_recordings_for_sermon,
    get_resources_for_sermon,
    get_bible_references_for_sermon,
    get_related_sermons_for_sermon,
)


console = Console()




def show(sermon_code: str):
    """Visa en specifik predikan, (identifierad av sermon-code)"""
    print(f"Visa predikan {sermon_code}")

    sermon = get_sermon_by_code(sermon_code)
    if not sermon:
        print(f"Predikan med kod {sermon_code} finns inte.")
        return

    services = get_services_for_sermon(sermon_code)
    manuscripts = get_manuscripts_for_sermon(sermon_code)
    recordings = get_recordings_for_sermon(sermon_code)
    resources = get_resources_for_sermon(sermon_code)
    bible_references = get_bible_references_for_sermon(sermon_code)
    related_sermons = get_related_sermons_for_sermon(sermon_code)

    width = shutil.get_terminal_size().columns - 4 #Get width of terminal window (with some margin)

    table = Table(title="Inspelningar")
    table.add_column("Typ")
    table.add_column("Datum")
    table.add_column("Fil")
    table.add_row("MP3", "2024-06-09", "p370.mp3")
    table.add_row("Video", "2024-06-09", "länk")
    console.print(table)

    
    body = (
        "[bold]Plats:[/bold] Storkyrkan\n"
        "[bold]Text:[/bold] Joh 3:16\n"
        "[bold]Betyg:[/bold] A\n\n"
        "Här kan själva predikotexten eller sammanfattningen visas."
    )
    console.print(Panel(Columns([body, table]), title="P370 – Nådens evangelium"))

    color = Color.from_rgb(100, 100, 100)
    color = Color.default()
    bgcolor = Color.from_rgb(0, 0, 0)
    bgcolor = Color.default()
    my_style = Style(color = Color.from_rgb(255, 0, 0), bold = True)
    title = f"[bold]{sermon_code}[/bold] ─── {sermon['title']}"
    subtitle = f"Oskar Fornander"

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
        manuscript_file_path = ARCHIVE_ROOT / Path('files/manuscripts/' + manuscript['file_name'])
        manuscript_txt = f"[link=file://{manuscript_file_path}]{manuscript['file_name']}[/link] ({manuscript['date']})"
        if manuscript['notes']:
            manuscript_txt += f" ({manuscript['notes']})"
        elements.append(manuscript_txt)

    for recording in recordings:
        recording_file_path = ARCHIVE_ROOT / Path('files/recordings/' + recording['file_name'])
        recording_txt = f"[link=file://{recording_file_path}]{recording['file_name']}[/link] ({recording['date']})"
        if recording['notes']:
            recording_txt += f" ({recording['notes']})"
        elements.append(recording_txt)




    console.print("[link=https://www.google.com]https://www.google.com[/link]")
    console.print("[link=https://www.google.com]länk[/link]")
    console.print('länk', style = "link https://www.google.com")






    body = Group(*elements)
    console.print(
        Panel(body,
            title = title,
            title_align = "left", 
            subtitle = subtitle,
            subtitle_align = "right",
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






#show('P401')
