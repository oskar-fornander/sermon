
from app.db import list_sermon_codes, list_service_dates, load_sermon_as_draft, get_sermon_code_by_service_date
from app.presentation.sermon_list import render_sermon_list


def list_sermons_by_code(n = 0, reverse = False):
    """Listar predikningar efter kod"""

    codes = list_sermon_codes()
    desc = 'Alla predikningar'
    if n > 0:  # If not show all (n=0 means --all)
        codes = codes[-n:]  # Crop the list to only include the number of sermons desired by the flag --limit/-n
        desc = f"De {min(n, len(codes))} senaste predikningarna"
    if reverse:
        codes.reverse()  #Reverse the sorted list if flag --reverse is set
    desc += " listade efter predikokod"

    sermons = []
    for code in codes:
        sermons.append(load_sermon_as_draft(code['code']))  # Get sermons as sermondDraft objects and store in a list

    render_sermon_list(title=desc, sermons=sermons, order_by='code')



def list_sermons_by_date(n = 0, reverse = False):
    """Listar predikningar efter predikodatum"""

    dates = list_service_dates()
    desc = 'Alla predikningar'
    if n > 0:  # If not show all (n=0 means --all)
        dates = dates[-n:]  # Crop the list to only include the number of sermons desired by the flag --limit/-n
        desc = f"De {min(n, len(dates))} senaste predikningarna"
    if reverse:
        dates.reverse()  #Reverse the sorted list if flag --reverse is set
    desc += " listade efter predikokod"

    sermons = []
    for date in dates:
        code = get_sermon_code_by_service_date(date['date'])  # Get code for the sermon at this date
        sermons.append(load_sermon_as_draft(code['code']))  # Get sermons as sermondDraft objects and store in a list

    render_sermon_list(title=desc, sermons=sermons, order_by='date')


