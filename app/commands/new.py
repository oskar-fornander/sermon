import typer
#from app.utils import CONFIG, ARCHIVE_ROOT
#from pathlib import Path
from app.db import get_last_sermon_code
from app.presentation.new_sermon import render_info_panel, user_input, show_sermon_draft
from rich.prompt import Prompt, Confirm
import re


pattern_code = re.compile(r'^P\d{3}$')  # Sermon code on this format: P372 etc



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

    default_code = 'P' + str(int(get_last_sermon_code()[1:]) + 1)  # Default code for new sermon: last code + 1

    render_info_panel('Ny predikan', 'För in uppgifter om predikan. Tryck enter för att acceptera default värde eller hoppa över.')

    code = user_input('Predikokod', default=default_code, pattern=pattern_code, allow_empty=False)
    print(f"--{code}--")
    title = user_input('Rubrik', allow_empty=False)
    print(f"--{title}--")


    context = Prompt.ask('Sammanhang')  # Get last sunday from evangelieboken.se?
    bible_references = Prompt.ask('Bibelreferenser (separera med semikolon)')
    introduktion = Prompt.ask('Introduktion')
    message = Prompt.ask('Budskap')
    report = Prompt.ask('Omdöme', choices=['A', 'B', 'C', ''], default='')
    related_sermon = Prompt.ask('Relaterad predikan (kod)')
    notes = Prompt.ask('Kommentar')


    service = Confirm.ask('Lägg till gudstjänst?', default=True)

    render_info_panel('Ny predikan', 'typ av inspelning?')
    recording_type = Prompt.ask('Typ', choices=['audio', 'video'], default='audio')






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
# 2. manuscript
#   file name (default)
#   date (default)
#   notes?
# 3. service?
#   date (default=last Sunday)
#   place (default=last place?)
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


