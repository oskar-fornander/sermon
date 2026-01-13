import typer
import shutil
from rich.console import Console
from rich.panel import Panel #https://rich.readthedocs.io/en/stable/reference/panel.html
from rich.text import Text
from rich.style import Style

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
    services = get_services_for_sermon(sermon_code)
    manuscripts = get_manuscripts_for_sermon(sermon_code)
    recordings = get_recordings_for_sermon(sermon_code)
    resources = get_resources_for_sermon(sermon_code)
    bible_references = get_bible_references_for_sermon(sermon_code)
    related_sermons = get_related_sermons_for_sermon(sermon_code)

    width = shutil.get_terminal_size().columns - 4 #Get width of terminal window (with some margin)

    
    body = (
        "[bold]Plats:[/bold] Storkyrkan\n"
        "[bold]Text:[/bold] Joh 3:16\n"
        "[bold]Betyg:[/bold] A\n\n"
        "Här kan själva predikotexten eller sammanfattningen visas."
    )
    console.print(Panel(body, title="P370 – Nådens evangelium"))

    console.print(Panel("innehåll ...", title=Text(text="P401", style=Style(bold = True)), title_align="left", subtitle="underrubrik", subtitle_align="right"))





#show('P401')
