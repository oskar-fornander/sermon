
import datetime
from app.db import query_sermons
from app.services.sermon_draft import load_sermon_as_draft
from app.presentation.sermon_list import render_sermon_list
from app.presentation.common import console
from app.utils import parse_month, validate_date


def search_sermons(search_term = '', list_by='code', n=0, offset=0, reverse = False, date_from = None, date_to = None, year = None, month = None, place = None, report = None, must_have_recording = False):  # List sermons by sermon code
    """Search and filter the sermons."""

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
    if not date_from:
        date_from = '1900-01-01'  # Universal start date for filtering search in database
    if not date_to:
        date_to = datetime.date.today().strftime('%Y-%m-%d')  # Universal end date


    result = query_sermons(sort=list_by, limit=n, offset=offset, query=search_term, date_from=date_from, date_to=date_to, year=year, month=month_index, place=place, report=report, must_have_recording=must_have_recording)


    from app.presentation.common import console
    console.print([r['code'] for r in result])

    # Build descriptive text to show above table
    desc = f"Sökresultat för sökning på: [key]{search_term}[/key]\n"
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
    for r in result:
        sermons.append(load_sermon_as_draft(r['code']))  # Get sermons as sermondDraft objects and store in a list
    if list_by == 'date':  # Dates for the services to show must be included when listed by date
        for r in result:
            dates.append(r['date'])

    render_sermon_list(title='Predikoarkiv – sökresultat', content=desc, sermons=sermons, dates=dates, order_by=list_by, reverse=reverse)





