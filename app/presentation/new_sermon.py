from app.presentation.common import *
from app.presentation.sermon_card import render_sermon_card



def show_sermon_draft(sermon_draft):
    """Show a sermon card for a draft, using an object instead of data from the databases."""
    render_sermon_card(sermon_draft, preview=True)  # Set preview to True to indicate it is a preview of a sermon


