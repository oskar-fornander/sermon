
from app.db import query_sermons, list_sermon_codes, list_service_dates, get_sermon_code_by_service_date
from app.services.sermon_draft import load_sermon_as_draft
from app.presentation.sermon_list import render_sermon_list
from app.errors import ValidationError


def list_sermons_by_code(n=0, reverse = False, year = None, month = None, place = None, report = None, must_have_recording = False):
    """Listar predikningar efter kod"""

    def parse_month(value: str) -> int:
        MONTH_MAP = {
            "1": 1, "01": 1, "jan": 1, "januari": 1,
            "2": 2, "02": 2, "feb": 2, "febr": 2, "februari": 2,
            "3": 3, "03": 3, "mar": 3, "mars": 3,
            "4": 4, "04": 4, "apr": 4, "april": 4,
            "5": 5, "05": 5, "maj": 5,
            "6": 6, "06": 6, "jun": 6, "juni": 6,
            "7": 7, "07": 7, "jul": 7, "juli": 7,
            "8": 8, "08": 8, "aug": 8, "augusti": 8,
            "9": 9, "09": 9, "sep": 9, "sept": 9, "september": 9,
            "10": 10, "okt": 10, "oktober": 10,
            "11": 11, "nov": 11, "november": 11,
            "12": 12, "dec": 12, "december": 12,
        }
        if not value:
            return None
        key = value.strip().lower()
        if key not in MONTH_MAP:
            raise ValidationError(f"Ogiltig månad: {value}")
        return MONTH_MAP[key]

    month_index = parse_month(month)

    result = query_sermons(query = None, year=year, month=month_index, place=place, report=report, must_have_recording=must_have_recording, limit=n, reverse=reverse)

    from app.presentation.common import console
    console.print([(r['code'], r['title']) for r in result])



#def list_sermons_by_date():
    #"""Listar predikningar efter predikodatum"""
#
    #pass


#def list_sermons_by_code(n = 0, reverse = False):
#    """Listar predikningar efter kod"""
#
#    codes = list_sermon_codes()
#    desc = 'Alla predikningar'
#    if n > 0:  # If not show all (n=0 means --all)
#        codes = codes[-n:]  # Crop the list to only include the number of sermons desired by the flag --limit/-n
#        desc = f"De {min(n, len(codes))} senaste predikningarna"
#    if reverse:
#        codes.reverse()  #Reverse the sorted list if flag --reverse is set
#    desc += " listade efter predikokod"
#
#    sermons = []
#    for code in codes:
#        sermons.append(load_sermon_as_draft(code['code']))  # Get sermons as sermondDraft objects and store in a list
#
#    render_sermon_list(title=desc, sermons=sermons, order_by='code')
#
#
#
def list_sermons_by_date(n = 0, reverse = False):
    """Listar predikningar efter predikodatum"""

    dates = list_service_dates()
    desc = 'Alla predikningar'
    if n > 0:  # If not show all (n=0 means --all)
        dates = dates[-n:]  # Crop the list to only include the number of sermons desired by the flag --limit/-n
        desc = f"De {min(n, len(dates))} senaste predikningarna"
    if reverse:
        dates.reverse()  #Reverse the sorted list if flag --reverse is set
    desc += " listade efter datum"

    sermons = []
    for date in dates:
        code = get_sermon_code_by_service_date(date['date'])  # Get code for the sermon at this date
        sermons.append(load_sermon_as_draft(code['code']))  # Get sermons as sermondDraft objects and store in a list

    render_sermon_list(title=desc, sermons=sermons, order_by='date')


