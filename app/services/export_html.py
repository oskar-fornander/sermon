#app/services/export_html.py
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List
from jinja2 import Environment, FileSystemLoader
from app.db import query_sermons
from app.config import PATH_HTML, USER, CLOUD_PROVIDER, CLOUD_MANUSCRIPTS, CLOUD_RECORDINGS, CLOUD_RESOURCES, HTML_REMOTE_DIR
from app.services.sermon_draft import load_sermon_as_draft, SermonDraft
from app.presentation.common import console
from app.services.upload import upload_file


@dataclass
class SermonDraftWithDate(SermonDraft):  # Extend SermonDraft to include date
    date: str = None
    all_dates: List[str] = None

@dataclass
class Cloud:
    provider: str
    manuscripts: str
    recordings: str
    resources: str

cloud = Cloud(provider=CLOUD_PROVIDER, manuscripts=CLOUD_MANUSCRIPTS, recordings=CLOUD_RECORDINGS, resources=CLOUD_RESOURCES)


def export_html():
    """Export the full sermon database as a html page."""

    data = query_sermons(sort='code', limit=0)  # Get all sermons in a list by code
    sermons = []
    for d in data:
        s = load_sermon_as_draft(d['code'])  # Make a SermonDraft object from each sermon. 

        # Replace non-existing values with '–' and joins lists
        s.context = s.context or '–'
        s.introduction = s.introduction or '–'
        s.message = s.message or '–'
        s.report = s.report or '–'
        s.notes = s.notes or '–'
        s.related_sermons = ', '.join(s.related_sermons) or '–'

        if len(s.services) == 0:  # Special case: no service, use date from  manuscript instead
            try:
                date = f"({s.manuscripts[0].date})"
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


    # Build html page:
    TEMPLATE_DIR = (Path(__file__).resolve().parent.parent / "templates")    
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('sermon.html.j2')

    # One for local use:
    html_local = template.render(
        sermons=sermons,
        user=USER,
        mode='local',
        cloud=cloud
    )

    file_local = PATH_HTML / 'sermon.local.html'
    with open(file_local, 'w', encoding='utf-8') as f:
        f.write(html_local)

    console.print(f"Export till html är klart: [link=file://{file_local}]{file_local}[/link]")

    # And one for online use:
    console.print('Laddar upp ...')
    html_web = template.render(  
        sermons=sermons,
        user=USER,
        mode='webb',
        cloud=cloud
    )

    file_web = PATH_HTML / 'sermon.web.html'
    with open(file_web, 'w', encoding='utf-8') as f:
        f.write(html_web)

    # Upload file with sftp
    try:
        remote_path = upload_file(file_web, HTML_REMOTE_DIR, 'index.html')
        console.print(f"Uppladdad till: [link={remote_path}]{remote_path}[/link]")
    except Exception as e:
        raise RuntimeError(f"Uppladdning med sftp misslyckades: {e}")

    



