from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, get_last_sunday, PATTERN
from app.db import delete_sermon_from_database, get_sermon_id
from app.presentation.common import console, clear_screen, render_info_panel, user_input, user_confirmation, user_choice
from app.presentation.sermon_card import render_sermon_card
from app.presentation.edit_sermon import render_edit_menu, user_edit_short_text, user_edit_short_text_list, user_edit_long_text, user_edit_services, user_edit_manuscripts, user_edit_recordings, user_edit_resources
from app.services.sermon_draft import deep_copy
import time


# Delete sermon from database


def delete_sermon(sermon_code: str):
    """Delete sermon"""

    if user_confirmation(f"Predikan [key]{sermon_code}[/key] och alla tillhörande filer kommer att raderas. Är du säker på att du vill fortsätta?", default = False):
        if user_confirmation(f"Denna åtgärd går inte att ångra; all data för [key]{sermon_code}[/key] kommer att försvinna. Radera?", default = False):
            id = get_sermon_id(sermon_code)
            delete_sermon_from_database(id)
            console.print(f"Predikan [key]{sermon_code}[/key] och alla tillhörande filer är raderade.")

