
from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, get_last_sunday, PATTERN
from app.db import get_last_sermon_code, get_all_sermon_codes
from app.presentation.common import console, clear_screen, render_info_panel, user_input, user_confirmation, user_choice
from app.presentation.new_sermon import show_sermon_draft
from app.presentation.edit_sermon import render_edit_menu


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

    while True:  # Loop until user exits edit mode

        clear_screen()  # Clear terminal window
        show_sermon_draft(sermon_draft)  # Show a preview of the draft 
        menu = ['Predikokod', 'Rubrik', 'Sammanhang', 'Bibelreferenser', 'Introduktion', 'Budskap', 'Omdöme', 'Kommentar', 'Gudstjänst', 'Manus', 'Inspelning', 'Resurs']
        render_edit_menu(title='Redigera predikan', options=menu)  # Show a menu for interactive editing
        choice = user_choice(title='Ditt val', options = [str(x + 1) for x in range(len(menu))] + ['s', 'q'], default = None)
        if choice == 's':
            #save and exit
            pass

        elif choice == 'q':
            #exit without saving
            pass

        option = menu[int(choice) - 1]
        print(option)


        # Redigering av långa texter - se chatGPT:s förslag: 2️⃣ Lösning A (rekommenderad): Öppna extern editor
        

        user_edit('2. Rubrik', sermon_draft.title)


        # + hjälptext ... ? Hjälp, och tips: Lämna tomt för att behålla värdet








