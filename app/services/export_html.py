#app/services/export_html.py
from jinja2 import Environment, FileSystemLoader
from app.db import query_sermons
from app.config import PATH_HTML



def export_html():
    """Export the full sermon database as a html page."""

    data = query_sermons(sort='code', limit=0)  # Get all sermons in a list
    sermons = []
    for s in data:
        sermons.append(load_sermon_as_draft(s['code']))  # as SermonDrafts


    # Build html page:
    env = Environment(loader=FileSystemLoader('app/templates'))
    template = env.get_template('sermon.html.j2')

    html = template.render(sermons=sermons)

    with open(PATH_HTML / 'sermon.html', 'w', encoding='utf-8') as f:
        f.write(html)






