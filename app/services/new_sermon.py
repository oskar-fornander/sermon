
from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, get_last_sunday, PATTERN
from app.db import get_last_sermon_code, get_all_sermon_codes, list_sermons
from app.presentation.common import console, render_info_panel, user_input, user_confirmation
from app.presentation.new_sermon import  show_sermon_draft


def new_sermon():
    """Skapa en ny predikan"""

    draft = {  # Save new sermon in a draft before writing to the database
        'sermon': None,
        'services': None,
        'manuscripts': None,
        'recordings': None,
        'resources': None,
        'bible_references': None,
        'related_sermons': None
    }

    render_info_panel('Ny predikan', 'För in uppgifter om predikan. Tryck enter för att acceptera default värde eller hoppa över.')
    sermon = {}

    # Start with sermon code and make sure it's unique and valid
    used_codes = get_all_sermon_codes()  # A new sermon code must be unique
    default_code = 'P' + str(int(get_last_sermon_code()[1:]) + 1)  # Default code for new sermon: last code + 1
    while True:
        code = user_input('Predikokod', default=default_code, pattern=PATTERN['code'], allow_empty=False)
        if code in used_codes:
            console.print(f"[bold red]Det finns redan en predikan med denna kod i databasen.[/bold red]")
        else:
            break
    sermon['code'] = code

    # Title
    sermon['title'] = user_input('Rubrik', allow_empty=False)

    # Context
    sermon['context'] = user_input('Sammanhang')  # Get last sunday from evangelieboken.se?

    # Bible references
    bible_references = []
    references = user_input('Bibelreferenser (separera med semikolon)')
    if references:
        references = references.split(';')
        for ref_text in references:
            reference = {}
            reference['reference_text'] = ref_text.strip()
            bible_references.append(reference)
        #print(bible_references)
    draft['bible_references'] = bible_references

    # Introduction
    sermon['introduction'] = user_input('Introduktion')

    # Message
    sermon['message'] = user_input('Budskap')

    # Report
    sermon['report'] = user_input('Omdöme', choices=['A', 'B', 'C'])  # allow_empty=True
    
    # Related sermon
    related_sermons = []
    sermons = user_input('Relaterad predikan (separera flera med semikolon)', pattern=PATTERN['related_sermons'])
    if sermons:
        sermons = sermons.split(';')
        for s in sermons:
            related = {}
            related['code'] = s.strip()
            related_sermons.append(related)
    draft['related_sermons'] = related_sermons

    # Notes
    sermon['notes'] = user_input('Kommentar')

    draft['sermon'] = sermon  # Add all basic sermon data to the draft

    # Add a service?
    add_service = user_confirmation('Lägga till gudstjänst?', default=True)
    services = []
    default_date = get_last_sunday() # Use last Sunday as the default date
    if add_service:
        service = {}  # Only a single service can be added here, use sermon attach service to add more
        default_place = list_sermons(order_by='date')[-1]['place']
        service['date'] = user_input('Datum (ÅÅÅÅ-MM-DD)', pattern=PATTERN['date'], default=default_date, allow_empty=False)
        default_date = service['date']  # Save to reuse later
        service['place'] = user_input('Plats', default=default_place, allow_empty=False)
        service['notes'] = user_input('Kommentar')
        services.append(service)
    draft['services'] = services

    # Manuscript
    manuscript = {}
    default_pdf = sermon['code'] + '.pdf'
    render_info_panel('Predikomanus', content=f"Filen (t.ex. {default_pdf}) ska placeras i mappen [link=file://{PATH_MANUSCRIPTS}]{PATH_MANUSCRIPTS}[/link]")
    manuscript['file_name'] = user_input('Filnamn', default=default_pdf, pattern=PATTERN['manuscript'], allow_empty=False, blank_line=False)
    manuscript['date'] = user_input('Datum', default=default_date, pattern=PATTERN['date'])
    manuscript['notes'] = user_input('Kommentar')
    draft['manuscripts'] = [manuscript]

    # Recording?
    add_recording = user_confirmation('Lägga till en inspelning?', default=True)
    default_recording = f"{default_date}_Predikan.mp3"
    recordings = []
    if add_recording:
        recording = {}  # Only a single recording can be added here, use sermon attach recording to add more
        render_info_panel('Inspelning', content=f"Ange datum för inspelning och typ (audio/video) och antingen extern url till källan eller filnamn till lokal fil. Filer med inspelningar (t.ex. {default_recording}) ska placeras i mappen [link=file://{PATH_RECORDINGS}]{PATH_RECORDINGS}[/link]")
        recording['date'] = user_input('Datum (ÅÅÅÅ-MM-DD)', pattern=PATTERN['date'], default=default_date, allow_empty=False, blank_line=False)
        recording['type'] = user_input('Typ', choices=['audio', 'video'], default='audio', allow_empty=False)
        source = user_input('Fil eller extern url?', choices=['fil', 'url'], default='fil')
        if source == 'fil':
            recording['file_name'] = user_input('Filnamn', default=default_recording, pattern=PATTERN['recording'], allow_empty=False)
        elif source == 'url':
            recording['external_url'] = user_input('URL',  pattern=PATTERN['url'], allow_empty=False)
        recording['notes'] = user_input('Kommentar')
        recordings.append(recording)
    draft['recordings'] = recordings


    # Resource?
    add_resource = user_confirmation('Lägga till en extra resurs?', default=False)
    resources = []
    if add_resource:
        render_info_panel('Extra resurs', content=f"De filer som utgör extra resurser (.pdf, .jpg, etc.) ska placeras i mappen [link=file://{PATH_RESOURCES}]{PATH_RESOURCES}[/link]")
        while add_resource:
            resource = {}
            resource['file_name'] = user_input('Filnamn', allow_empty=False, blank_line=False)
            resource['title'] = user_input('Rubrik')
            resource['notes'] = user_input('Kommentar')
            resources.append(resource)
            add_resource = user_confirmation('Lägga till ytterligare en extra resurs?', default=False)
    draft['resources'] = resources

    # All added
    # Show a preview of the draft before saving
    show_sermon_draft(draft)

    if user_confirmation('Spara predikan?', default=True):
        print('save ...')

        updated_sermon_draft = interactive_edit_sermon(draft)
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

