
from app.db import query_sermons, query_services, list_sermon_codes, list_service_dates, get_sermon_code_by_service_date
from app.services.sermon_draft import load_sermon_as_draft
from app.presentation.sermon_list import render_sermon_list
from app.errors import ValidationError


def list_sermons(list_by='code', n=0, offset=0, reverse = False, year = None, month = None, place = None, report = None, must_have_recording = False):
    """List sermons by code or date"""
    if list_by == 'date':
        pass
        query_services()

    month_index = parse_month(month)

    result = query_sermons(query = None, year=year, month=month_index, place=place, report=report, must_have_recording=must_have_recording, limit=n, offset=offset)

    from app.presentation.common import console
    console.print([(r['code'], r['title']) for r in result])

    # Build descriptive text to show above table
    desc = 'Alla predikningar'
    if n > 0:  # If not show all (n=0 means --all)
        desc = f"De {min(n, len(result))} senaste predikningarna"
        if offset > 0:
            desc += f" (offset: {offset})"
    if list_by == 'date':
        desc += " listade efter datum.\n"
    else:
        desc += " listade efter predikokod.\n"
    desc += f"Filter: "
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
    for r in result:
        sermons.append(load_sermon_as_draft(r['code']))  # Get sermons as sermondDraft objects and store in a list

    render_sermon_list(title=desc, sermons=sermons, order_by='code', reverse=reverse)




def parse_month(value: str) -> int:
    MONTH_MAP = {
        "1": 1, "01": 1, "jan": 1, "januari": 1, "january": 1,
        "2": 2, "02": 2, "feb": 2, "febr": 2, "februari": 2, "february": 2,
        "3": 3, "03": 3, "mar": 3, "mars": 3, "march": 3,
        "4": 4, "04": 4, "apr": 4, "april": 4,
        "5": 5, "05": 5, "maj": 5, "may": 5,
        "6": 6, "06": 6, "jun": 6, "juni": 6, "june": 6,
        "7": 7, "07": 7, "jul": 7, "juli": 7, "july": 7,
        "8": 8, "08": 8, "aug": 8, "augusti": 8, "august": 8,
        "9": 9, "09": 9, "sep": 9, "sept": 9, "september": 9,
        "10": 10, "okt": 10, "oktober": 10, "october": 10,
        "11": 11, "nov": 11, "november": 11,
        "12": 12, "dec": 12, "december": 12,
    }
    if not value:
        return None
    key = value.strip().lower()
    if key not in MONTH_MAP:
        raise ValidationError(f"Ogiltig månad: {value}")
    return MONTH_MAP[key]






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
