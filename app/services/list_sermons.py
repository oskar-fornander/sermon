
from app.db import query_sermons, query_services, list_sermon_codes, list_service_dates, get_sermon_code_by_service_date
from app.services.sermon_draft import load_sermon_as_draft
from app.presentation.sermon_list import render_sermon_list
from app.errors import ValidationError
from app.utils import parse_month


def list_sermons(list_by='code', n=0, offset=0, reverse = False, year = None, month = None, place = None, report = None, must_have_recording = False):
    """List sermons by code or date"""

    month_index = parse_month(month)

    if list_by not in ('code', 'date'):
        raise ValidationError(f"Invalid value of argument list_by: {list_by} Must be 'code' or 'date'")

    result = query_sermons(sort=list_by, limit=n, offset=offset, query = None, year=year, month=month_index, place=place, report=report, must_have_recording=must_have_recording)

    from app.presentation.common import console
    console.print([r['code'] for r in result])

    # Build descriptive text to show above table
    desc = f"Alla ({len(result)}) predikningar"
    if n > 0:  # If not show all (n=0 means --all)
        desc = f"De {min(n, len(result))} senaste predikningarna"
        if offset > 0:
            desc += f" (offset: {offset})"
    if list_by == 'date':
        desc += " listade efter datum."
    else:
        desc += " listade efter predikokod."
    desc += f"\n{n=} "
    if offset > 0:
        desc += f"{offset=}"
    desc += f"\nFilter: "
    if year:
        desc += f"{year=} "
    if month:
        desc += f"{month=} "
    if place:
        desc += f"{place=} "
    if report:
        desc += f"{report=} "
    if must_have_recording:
        desc += f"has-recording={must_have_recording} "


    sermons = []
    dates = []
    for r in result:
        sermons.append(load_sermon_as_draft(r['code']))  # Get sermons as sermondDraft objects and store in a list
    if list_by == 'date':  # Dates for the services to show must be included when listed by date
        for r in result:
            dates.append(r['date'])

    render_sermon_list(title='Predikoarkiv – listar predikningar', content=desc, sermons=sermons, dates=dates, order_by=list_by, reverse=reverse)







#def list_sermons_by_date():
    #"""Listar predikningar efter predikodatum"""
#
    #pass


#
#
#def list_sermons_by_date(n = 0, reverse = False):
#    """Listar predikningar efter predikodatum"""
#
#    dates = list_service_dates()
#    desc = 'Alla predikningar'
#    if n > 0:  # If not show all (n=0 means --all)
#        dates = dates[-n:]  # Crop the list to only include the number of sermons desired by the flag --limit/-n
#        desc = f"De {min(n, len(dates))} senaste predikningarna"
#    if reverse:
#        dates.reverse()  #Reverse the sorted list if flag --reverse is set
#    desc += " listade efter datum"
#
#    sermons = []
#    for date in dates:
#        code = get_sermon_code_by_service_date(date['date'])  # Get code for the sermon at this date
#        sermons.append(load_sermon_as_draft(code['code']))  # Get sermons as sermondDraft objects and store in a list
#
#    render_sermon_list(title=desc, sermons=sermons, order_by='date')
#
#
