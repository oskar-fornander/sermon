
from app.config import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from app.utils import get_last_sunday, PATTERN
from app.services.sermon_draft import new_sermon_draft, new_service_draft, new_manuscript_draft, new_recording_draft, new_resource_draft, create_sermon_from_draft
from app.db import get_last_sermon_code, get_all_sermon_codes, get_last_place, update_sermon_from_draft
from app.presentation.common import console, render_info_panel, user_input, user_confirmation
from app.presentation.new_sermon import  show_sermon_draft
from app.services.edit_sermon import interactive_edit_sermon


def new_sermon():
    """Skapa en ny predikan"""
    # Enter sermon code and Title and then enter into interactive edit mode to get a good overview of the editing of the new sermon before saving as a new sermon

    sermon_draft = new_sermon_draft()  # Save new sermon in a draft before writing to the database

    render_info_panel('Ny predikan', 'För in uppgifter om ny predikan.') 

    # Start with sermon code and make sure it's unique and valid
    used_codes = get_all_sermon_codes()  # A new sermon code must be unique
    default_code = 'P' + f"{int(get_last_sermon_code()[1:]) + 1:03d}"  # Default code for new sermon: last code + 1, as three digits with leading zeros
    while True:
        code = user_input('Predikokod', default=default_code, pattern=PATTERN['code'], pattern_example=f"t.ex. {default_code}", allow_empty=False)
        if code in used_codes:
            console.print(f"[alert]Det finns redan en predikan med denna kod i databasen.[/alert]")
        else:
            break
    sermon_draft.code = code

    # Title
    sermon_draft.title = user_input('Rubrik', allow_empty=False).strip()


    # Enter interactive editing mode to fill in the rest 
    #show_sermon_draft(sermon_draft)
    updated_sermon_draft = interactive_edit_sermon(sermon_draft)

    if updated_sermon_draft:
        create_sermon_from_draft(updated_sermon_draft)
        console.print(f"Predikan [key]{updated_sermon_draft.code}[/key] är sparad. visa med [code]sermon show {updated_sermon_draft.code}[/code]")
    else:
        # Do not save a new sermon
        console.print(f"Predikan har inte sparats.")

    return

        
