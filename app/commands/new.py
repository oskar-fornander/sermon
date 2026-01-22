import typer
#from app.utils import CONFIG, ARCHIVE_ROOT
#from pathlib import Path
from app.db import get_last_sermon_code, get_all_sermon_codes
from app.presentation.new_sermon import render_info_panel, user_input, show_sermon_draft
from app.presentation.common import console
from rich.prompt import Prompt, Confirm
import re


pattern_code = re.compile(r'^P\d{3}$')  # Sermon code on this format: P372 etc
pattern_related_sermons = re.compile(r'^P\d{3}((\s*\;\s*)(P\d{3}))*$') # P001; P002 etc



def new():
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
        code = user_input('Predikokod', default=default_code, pattern=pattern_code, allow_empty=False)
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
    sermon['introduktion'] = user_input('Introduktion')

    # Message
    sermon['message'] = user_input('Budskap')

    # Report
    sermon['report'] = user_input('Omdöme', choices=['A', 'B', 'C'])  # allow_empty=True
    
    # Related sermon
    related_sermons = []
    sermons = user_input('Relaterad predikan (separera flera med semikolon)', pattern=pattern_related_sermons)
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
    print(draft)

    # Add a service?
    service = Confirm.ask('Lägga till gudstjänst?', default=True)


# 2. service?
#   date (default=last Sunday)
#   place (default=last place?)
#   notes?
# 3. manuscript
#   file name (default)
#   date (default)
#   notes?







    return



    show_sermon_draft(draft)
    if Confirm.ask('Spara predikan?', default='Y'):
        pass


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
# 
#   
# 
# 
# 
# 
# 
# 
# 


