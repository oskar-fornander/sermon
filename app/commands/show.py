import typer
from app.utils import CONFIG, ARCHIVE_ROOT
from pathlib import Path
from app.presentation.sermon_card import render_sermon_card

from app.db import get_sermon_by_code, get_services_for_sermon, get_manuscripts_for_sermon, get_recordings_for_sermon, get_resources_for_sermon, get_bible_references_for_sermon, get_related_sermons_for_sermon

def show(sermon_code: str):
    """Visa en specifik predikan, (identifierad av sermon-code)"""
    #print(f"Visa predikan {sermon_code}")

    sermon = get_sermon_by_code(sermon_code)
    if not sermon:
        print(f"Predikan med kod {sermon_code} finns inte.")
        return

    services = get_services_for_sermon(sermon_code)
    manuscripts = get_manuscripts_for_sermon(sermon_code)
    recordings = get_recordings_for_sermon(sermon_code)
    resources = get_resources_for_sermon(sermon_code)
    bible_references = get_bible_references_for_sermon(sermon_code)
    related_sermons = get_related_sermons_for_sermon(sermon_code)

    render_sermon_card(
            sermon=sermon, 
            services=services, 
            manuscripts=manuscripts, 
            recordings=recordings, 
            resources=resources, 
            bible_references=bible_references, 
            related_sermons=related_sermons)

