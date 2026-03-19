
from app.db import query_sermons
from app.presentation.common import console


def search_sermons(search_term):
    """Search and filter the sermons."""
    pass

    # send parameters as lower case?

    result = query_sermons(query=search_term)

    console.print([(r['code'], r['title']) for r in result])



