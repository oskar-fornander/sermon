#app/services/export_html.py
from dataclasses import dataclass, asdict
from jinja2 import Environment, FileSystemLoader
from app.db import query_sermons
from app.config import PATH_HTML
from app.services.sermon_draft import load_sermon_as_draft, SermonDraft
from app.presentation.common import console


@dataclass
class SermonDraftWithDate(SermonDraft):  # Extend SermonDraft to include date
    date: str = None




def export_html():
    """Export the full sermon database as a html page."""

    data = query_sermons(sort='date', limit=0)  # Get all sermons in a list

# Hämta med sort='code' istället och lägg till nya objekt för varje service och sortera sedan?

    sermons = []
    for s in data:
        sermon = load_sermon_as_draft(s['code'])  # Make a SermonDraft object from each sermon. There may be duplicates if a sermon has more than one service
        sermon = SermonDraftWithDate(**asdict(sermon), date=s['date'])  # Add date to object by extending it to a new dataclass
        sermons.append(sermon)  # as SermonDrafts
    console.print(sermons[0])

    # Build html page:
    env = Environment(loader=FileSystemLoader('app/templates'))
    template = env.get_template('sermon.html.j2')

    html = template.render(
        sermons=sermons
    )

    file = PATH_HTML / 'sermon.html'
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

    console.print(f"Export till html är klart: [link=file://{file}]{file}[/link]")





