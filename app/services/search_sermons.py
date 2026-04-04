
import datetime
import re
from app.db import query_sermons
from app.services.sermon_draft import load_sermon_as_draft
from app.presentation.sermon_list import render_sermon_list
from app.presentation.sermon_card import render_sermon_card
from app.presentation.common import console, user_confirmation, user_input, render_info_panel, clear_screen
from app.utils import parse_month, validate_date, parse_sermon_code


def search_sermons(query = [], list_by='code', n=0, offset=0, reverse = False, bible_only = False, date_from = None, date_to = None, year = None, month = None, place = None, report = None, must_have_recording = False):  # List sermons by sermon code
    """Search and filter the sermons."""

    search_text = ', '.join(["'[key]" + s + "[/key]'" for s in query])
    console.print(f"Sök på {search_text} bland predikningarna")

    month_index = parse_month(month)

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


    result = query_sermons(sort=list_by, limit=n, offset=offset, query=query, bible_only=bible_only, date_from=date_from, date_to=date_to, year=year, month=month_index, place=place, report=report, must_have_recording=must_have_recording)


    #console.print([r['code'] for r in result])

    # Build descriptive text to show above table
    desc = f"Sökresultat för sökning på: {search_text}\n"
    desc += f"Träff i {len(result)} predikningar\n"
    if n > 0:  # If not show all (n=0 means --all)
        desc += f"Begränsat till {n} träffar"
        if offset > 0:
            desc += f" (offset: {offset})"
        desc += '. '
    if list_by == 'date':
        desc += "Listade efter datum"
    else:
        desc += "Listade efter predikokod"
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
    codes = []
    for r in result:
        codes.append(r['code'])
        sermons.append(load_sermon_as_draft(r['code']))  # Get sermons as sermondDraft objects and store in a list
    if list_by == 'date':  # Dates for the services to show must be included when listed by date
        for r in result:
            dates.append(r['date'])


    pattern = re.compile(r'(^P?\d{3}$|^[qa]$)', re.IGNORECASE)  # Sermon codes or abort
    while True:
        render_sermon_list(title='Predikoarkiv – sökresultat', content=desc, sermons=sermons, dates=dates, order_by=list_by, reverse=reverse)
        if len(sermons) < 1:
            return

        render_info_panel('Granska sökresultatet', 'Ange kod för en predikan att granska eller [key]q[/key] för att avbryta.', '', blank_line = False)
        code = ''
        while code not in codes:
            code = user_input('Predikokod', pattern=pattern, allow_empty=False, blank_line=True)
            if code in 'Qq':  # Quit
                return
            code = parse_sermon_code(code, raiseError=False)  # Make sure code is in correct format or none
            if not code:
                continue
            console.print(f"Predikan [error]{code}[/error] finns inte i listan med sökresultat.")

        clear_screen()
        render_sermon_card(sermons[codes.index(code)], query=query) 
        while not user_confirmation('Fortsätta?', default=True, blank_line=False):
            pass
        clear_screen()


    

    




