
import datetime
from app.db import query_sermons, query_services, list_sermon_codes, list_service_dates, get_sermon_code_by_service_date
from app.services.sermon_draft import load_sermon_as_draft
from app.presentation.sermon_list import render_sermon_list
from app.errors import ValidationError
from app.utils import parse_month, PATTERN, validate_date


def list_sermons(list_by='code', n=0, offset=0, reverse = False, date = None, date_from = None, date_to = None, year = None, month = None, place = None, report = None, must_have_recording = False):
    """List sermons by code or date"""

    month_index = parse_month(month)
    if not date is None:
        validate_date(date)  # Raise an error if date is invalid. If a valid date is given as an argument then year and month are ignored in the filtering
        year = None
        month = None

    if list_by not in ('code', 'date'):
        raise ValidationError(f"Invalid value of argument list_by: {list_by} Must be 'code' or 'date'")

    # Validate --from and --to dates
    if date_from:
        validate_date(date_from)  # If dates are not in ISO format YYYY-MM-DD an error is raised
    if date_to:
        validate_date(date_to)
    if date_from and date_to and date_from > date_to:
        #raise ValidationError('Datumfel: --from måste vara före --to')  # Raise an error if in wrong order
        date_from, date_to = date_to, date_from  # Simply swap them?


    result = query_sermons(sort=list_by, limit=n, offset=offset, query = None, date=date, date_from=date_from, date_to=date_to, year=year, month=month_index, place=place, report=report, must_have_recording=must_have_recording)


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
    desc += f"\nAntal: {n} \n"
    if offset > 0:
        desc += f"{offset=}"
    if date_from and date_to:
        desc += f"Period: {date_from} – {date_to}"
    elif date_from:
        desc += f"Period: från {date_from}"
    elif date_to:
        desc += f"Period: till {date_to}"
    else:
        desc += 'Period: –'
    desc += f"\nFilter: "
    if date:
        desc += f"{date=} "
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
