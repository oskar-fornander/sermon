
from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, get_last_sunday, PATTERN
from app.db import get_last_sermon_code, get_all_sermon_codes, list_sermons
from app.presentation.common import console, render_info_panel, user_input, user_confirmation
from app.presentation.new_sermon import show_sermon_draft


def edit_service():
    """Redigera gudstjänst"""



