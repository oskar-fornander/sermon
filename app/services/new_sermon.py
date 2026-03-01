
from app.config import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from app.utils import get_last_sunday, PATTERN
from app.services.sermon_draft import new_sermon_draft, new_service_draft, new_manuscript_draft, new_recording_draft, new_resource_draft
from app.db import get_last_sermon_code, get_all_sermon_codes, get_last_place, create_sermon_from_draft, update_sermon_from_draft
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
        code = user_input('Predikokod', default=default_code, pattern=PATTERN['code'], allow_empty=False)
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

        
    # ############################################## #
    # #### BELOW: Old version with procedural entering of values instead of interactive editing #### #





    # Context
    sermon_draft.context = user_input('Sammanhang')  # Get last sunday from evangelieboken.se?

    # Bible references
    bible_references = []
    references = user_input('Bibelreferenser', description=' (separera med semikolon)')
    if references:
        # TODO: Validate bible references
        references = references.split(';')
        for ref_text in references:
            bible_references.append(ref_text.strip())
        #print(bible_references)
    sermon_draft.bible_references = bible_references

    # Introduction
    sermon_draft.introduction = user_input('Introduktion')

    # Message
    sermon_draft.message = user_input('Budskap')

    # Report
    sermon_draft.report = user_input('Omdöme', choices=['A', 'B', 'C'])  # allow_empty=True
    
    # Related sermon
    related_sermons = []
    sermons = user_input('Relaterad predikan', description=' (separera flera med kommatecken)', pattern=PATTERN['related_sermons'])
    if sermons:
        sermons = sermons.split(',')
        for s in sermons:
            related_sermons.append(s.strip())
    sermon_draft.related_sermons = related_sermons

    # Notes
    sermon_draft.notes = user_input('Kommentar')


    # Add a service?
    add_service = user_confirmation('Lägga till gudstjänst?', default=True)
    default_date = get_last_sunday() # Use last Sunday as the default date
    if add_service:
        service_draft = new_service_draft()  # Only a single service can be added here, use sermon attach service to add more
        #default_place = list_sermons(order_by='date')[-1]['place']
        default_place = get_last_place()  # Get the place of the last service
        service_draft.date = user_input('Datum', description=' (ÅÅÅÅ-MM-DD)', pattern=PATTERN['date'], default=default_date, allow_empty=False)
        default_date = service_draft.date  # Save to reuse later
        service_draft.place = user_input('Plats', default=default_place, allow_empty=False)
        service_draft.notes = user_input('Kommentar')
        sermon_draft.services.append(service_draft)

    # Manuscript
    manuscript_draft = new_manuscript_draft()
    default_pdf = sermon_draft.code + '.pdf'
    render_info_panel('Predikomanus', content=f"Filen (t.ex. {default_pdf}) ska placeras i mappen [link=file://{PATH_MANUSCRIPTS}]{PATH_MANUSCRIPTS}[/link]")
    manuscript_draft.file_name = user_input('Filnamn', default=default_pdf, pattern=PATTERN['manuscript'], allow_empty=False, blank_line=False)
    manuscript_draft.date = user_input('Datum', default=default_date, pattern=PATTERN['date'])
    manuscript_draft.notes = user_input('Kommentar')
    sermon_draft.manuscripts.append(manuscript_draft)

    # Recording?
    add_recording = user_confirmation('Lägga till en inspelning?', default=True)
    default_recording = f"{default_date}_Predikan.mp3"
    if add_recording:
        recording_draft = new_recording_draft()  # Only a single recording can be added here, use sermon attach recording to add more
        render_info_panel('Inspelning', content=f"Ange datum för inspelning och typ (audio/video) och antingen extern url till källan eller filnamn till lokal fil. Filer med inspelningar (t.ex. {default_recording}) ska placeras i mappen [link=file://{PATH_RECORDINGS}]{PATH_RECORDINGS}[/link]")
        recording_draft.date = user_input('Datum', description=' (ÅÅÅÅ-MM-DD)', pattern=PATTERN['date'], default=default_date, allow_empty=False, blank_line=False)
        recording_draft.type = user_input('Typ', choices=['audio', 'video'], default='audio', allow_empty=False)
        source = user_input('Fil eller extern url?', choices=['fil', 'url'], default='fil')
        if source == 'fil':
            recording_draft.file_name = user_input('Filnamn', default=default_recording, pattern=PATTERN['recording'], allow_empty=False)
        elif source == 'url':
            recording_draft.external_url = user_input('URL',  pattern=PATTERN['url'], allow_empty=False)
        recording_draft.notes = user_input('Kommentar')
        sermon_draft.recordings.append(recording_draft)


    # Resource?
    add_resource = user_confirmation('Lägga till en extra resurs?', default=False)
    if add_resource:
        render_info_panel('Extra resurs', content=f"De filer som utgör extra resurser (.pdf, .jpg, etc.) ska placeras i mappen [link=file://{PATH_RESOURCES}]{PATH_RESOURCES}[/link]")
        while add_resource:
            resource_draft = new_resource_draft()
            resource_draft.file_name = user_input('Filnamn', allow_empty=False, blank_line=False)
            resource_draft.title = user_input('Rubrik')
            resource_draft.notes = user_input('Kommentar')
            sermon_draft.resources.append(resource_draft)
            add_resource = user_confirmation('Lägga till ytterligare en extra resurs?', default=False)

    # All added
    # Show a preview of the draft before saving
    show_sermon_draft(sermon_draft)

    if user_confirmation('Spara predikan?', default=True):
        print('save ...')

        updated_sermon_draft = interactive_edit_sermon(sermon_draft)
        create_sermon_from_draft(updated_sermon_draft)

        


# Enter to accept default or empty
# 
# 1. Basic info:
#   code
#   title
#   context
#   bible references *
#   introduction
#   message
#   report
#   related sermon *
#   notes
# 2. service?
#   date (default=last Sunday)
#   place (default=last place?)
#   notes?
# 3. manuscript
#   file name (default)
#   date (default)
#   notes?
# 4. recording?
#   date (default)
#   type
#   file or external link?
#   file name/external link
#   notes?
# 5. resource? (allow more than one)
#   file name
#   title
#   notes?

