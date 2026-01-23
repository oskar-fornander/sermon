from app.presentation.common import *
from app.presentation.sermon_card import render_sermon_card



def show_sermon_draft(draft):
    """Show a sermon card for a draft, using an object instead of data from the databaes."""
    render_sermon_card(
            sermon=draft['sermon'], 
            services=draft['services'], 
            manuscripts=draft['manuscripts'], 
            recordings=draft['recordings'], 
            resources=draft['resources'], 
            bible_references=draft['bible_references'], 
            related_sermons=draft['related_sermons'],
            draft=True)  # Set draft to True to indicate it is a preview of a sermon


