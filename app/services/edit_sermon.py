
from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, get_last_sunday, PATTERN
from app.db import get_last_sermon_code, get_all_sermon_codes, list_sermons
from app.presentation.common import console, render_info_panel, user_input, user_confirmation
from app.presentation.new_sermon import show_sermon_draft



def update_sermon_code(sermon_code: str, code: str):
    """Ändra predikans kod"""
    pass
def update_sermon_title(sermon_code: str, title: str):
    """Ändra predikans titel"""
    pass

def update_sermon_context(sermon_code: str, context: str):
    """Ändra predikans sammanhang"""
    pass

def update_sermon_introduction(sermon_code: str, introduction: str):
    """Ändra predikans introduktion"""
    pass

def update_sermon_message(sermon_code: str, message: str):
    """Ändra predikans budskap"""
    pass

def update_sermon_report(sermon_code: str, report: str):
    """Ändra predikans omdöme"""
    pass

def update_sermon_notes(sermon_code: str, notes: str):
    """Ändra predikans kommentar"""
    pass




# ---------- Interactive edit ---------- #
def interactive_edit_sermon(draft):
    """Interaktiv redigering av predikan"""
    pass

