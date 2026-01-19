
from app.presentation.common import *


def render_sermon_list(sermons, services = None, order_by = 'code'):
    """Render a presentation of a list of sermons, sorted by code or date."""

    for i in range(len(sermons)):
        sermon = sermons[i]

        if order_by == 'date':
            txt = f"{sermon['code']} {sermon['date']} {sermon['place']} {sermon['title']}"
            print(txt)
        else: #code
            service = ''
            if services and services[i]:
                service = ', '.join([s['date'] for s in services[i]][::-1]) #Show all services in descending order
            print(f"{sermon['code']} {sermon['title']} {service}")







