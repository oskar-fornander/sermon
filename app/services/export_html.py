#app/services/export_html.py
from dataclasses import dataclass, asdict
from typing import List
from jinja2 import Environment, FileSystemLoader
from app.db import query_sermons
from app.config import PATH_HTML
from app.services.sermon_draft import load_sermon_as_draft, SermonDraft
from app.presentation.common import console


@dataclass
class SermonDraftWithDate(SermonDraft):  # Extend SermonDraft to include date
    date: str = None
    all_dates: List[str] = None




def export_html():
    """Export the full sermon database as a html page."""

    data = query_sermons(sort='code', limit=0)  # Get all sermons in a list by code
    sermons = []
    for d in data:
        s = load_sermon_as_draft(d['code'])  # Make a SermonDraft object from each sermon. 

        if len(s.services) == 0:  # Special case: no service, use date from  manuscript instead
            try:
                date = s.manuscripts[0].date
            except Exception:
                date = ''
            sermon = SermonDraftWithDate(**asdict(s), date=date, all_dates=[])  # Add date to object by extending it to a new dataclass
            sermons.append(sermon)
        else:
            all_dates = []
            for service in s.services:  # Add date for each service. There may be duplicates if a sermon has more than one service
                all_dates.append(service.date)  # Save all dates for a sermon in each instance of that sermon
            all_dates.sort()
            all_dates = all_dates[::-1]  # Sort dates in reversed order
            for date in all_dates:
                sermon = SermonDraftWithDate(**asdict(s), date=date, all_dates=all_dates)  # Add date to object by extending it to a new dataclass
                sermons.append(sermon)

    #console.print(sermons[0])

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





