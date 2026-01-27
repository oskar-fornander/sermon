
from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, get_last_sunday, PATTERN
from app.db import get_last_sermon_code, get_all_sermon_codes
from app.presentation.common import console, clear_screen, render_info_panel, user_input, user_confirmation, user_choice
from app.presentation.new_sermon import show_sermon_draft
from app.presentation.edit_sermon import render_edit_menu, user_edit_short_text, user_edit_short_text_list, user_edit_long_text, user_edit_services, user_edit_manuscripts, user_edit_recordings, user_edit_resources
from app.services.sermon_draft import deep_copy
import time


# interactive_edit_sermon() down below


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
def interactive_edit_sermon(sermon_draft):
    """Interaktiv redigering av predikan"""

    EDIT_FIELDS = {
        'Predikokod': ('code', user_edit_short_text),
        'Rubrik': ('title', user_edit_short_text),
        'Sammanhang': ('context', user_edit_short_text),
        'Bibelreferenser': ('bible_references', user_edit_short_text_list),
        'Introduktion': ('introduction', user_edit_long_text),
        'Budskap': ('message', user_edit_long_text),
        'Kommentar': ('notes', user_edit_short_text),
        'Omdöme': ('report', user_edit_short_text),
        'Gudstjänst': ('services', user_edit_services),
        'Manus': ('manuscripts', user_edit_manuscripts),
        'Inspelning': ('recordings', user_edit_recordings),
        'Resurs': ('resources', user_edit_resources)
    }
    menu = list(EDIT_FIELDS.keys())  # A list of all menu options based on keys in dict

    while True:  # Loop until user exits edit mode
        clear_screen()  # Clear terminal window
        show_sermon_draft(sermon_draft)  # Show a preview of the draft 
        render_edit_menu(title='Redigera predikan', options=menu)  # Show a menu for interactive editing
        choice = user_choice(title='Ditt val', options = [str(x + 1) for x in range(len(menu))] + ['s', 'q'], default = None)

        if not choice:
            continue
        
        if choice == 's':
            #save and exit
            return sermon_draft  # Updated version is returned

        elif choice == 'q':
            #exit without saving
            return None

        option = menu[int(choice) - 1]  # A numerical choice from the menu
        field_name, editor = EDIT_FIELDS[option]  # Select field to edit and edit function to use
        current_value = deep_copy(getattr(sermon_draft, field_name))

        if option == 'Predikokod':  # Special case: sermon code. Make sure the sermon code is unique and valid
            used_codes = get_all_sermon_codes()  # A new sermon code must be unique
            while True:
                new_value = user_edit_short_text(sermon_draft.code, 'Predikokod', current_value, pattern=PATTERN['code'])
                if not new_value:  # no value no change
                    break
                if new_value in used_codes:
                    console.print(f"[bold red]Det finns redan en predikan med denna kod i databasen.[/bold red]")
                else:
                    break
        elif option == 'Omdöme':  # Special case: report. Limit options to valid reports
            new_value = user_edit_short_text(sermon_draft.code, 'Omdöme', current_value, choices=['A', 'B', 'C', '-'])
        else:  # All other fields than sermon code
            new_value = editor(sermon_draft.code, option, current_value)  # Get new value with the desired editor function


        # Update value
        if new_value:
            if new_value == '-':  # Leave field empty (if allowed)
                if field_name in ['context', 'bible_references', 'introduction', 'message', 'notes', 'report']:  # Only these fields may be empty
                    setattr(sermon_draft, field_name, '')  # Clear value in sermon draft
                else:
                    console.print('Detta fält får inte vara tomt')
            else:
                setattr(sermon_draft, field_name, new_value)  # Update value in sermon draft
                console.print('Uppdaterat')
        else:
            console.print('Ej uppdaterat')
        time.sleep(1)


