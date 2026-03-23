
from app.db import query_sermons
from app.presentation.common import console


def search_sermons(search_term = '', list_by='code', n=0, offset=0, reverse = False, year = None, month = None, place = None, report = None, must_have_recording = False):  # List sermons by sermon code
    """Search and filter the sermons."""

    # send parameters as lower case?

    result = query_sermons(query=search_term)

    console.print([r['code'] for r in result])



