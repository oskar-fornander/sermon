#app/services/open.py
import subprocess
from app.utils import parse_sermon_code
from app.presentation.common import clear_screen, console, user_choice
from app.config import APP_PDF, APP_AUDIO, APP_VIDEO, APP_URL, PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from app.db import get_manuscripts_for_sermon, get_recordings_for_sermon, get_resources_for_sermon



def open_manuscript(sermon_code: str):
    """Open manuscript for sermon"""
    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format
    console.print(f"Öppna manus till predikan {sermon_code}")

    manuscripts = get_manuscripts_for_sermon(sermon_code)

    i = 1
    if len(manuscripts) > 1:
        txt = ''
        for i, m in enumerate(manuscripts):
            txt += f"\n[key]{i + 1}.[/key] [title]{m['file_name']}[/title], {m['date']} "
            if m['notes']:
                txt += f"[notes]({m['notes']})[/notes]"
        console.print(txt + '\n')
        i =  int(user_choice(title='Välj manus att öppna', options=[str(i) for i in range(1, len(manuscripts) + 1)]))
    
    file_name = manuscripts[i - 1]['file_name']
    path = PATH_MANUSCRIPTS / file_name

    console.print(f"Öppnar {file_name} med {APP_PDF} ...")

    if APP_PDF:
        subprocess.run(['open', '-a', APP_PDF, path])
    else:
        subprocess.run(['open', path])






def open_recording(sermon_code: str):
    """Open recording for sermon"""
    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format
    console.print(f"Öppna inspelning till predikan {sermon_code}")



def open_resource(sermon_code: str):
    """Open resource for sermon"""
    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format
    console.print(f"Öppna resurs till predikan {sermon_code}")




## add a service layer ...
#
#    #välj om det finns flera inspelningar/filer: 1. datum, 2. datum, etc.
#
#    # Ange fel om ingen fil ska finnas
#    # Ange fel om fil saknas på disk
#
#    # audio or video?
#
#    path = ''
#    subprocess.run(['open', '-a', APP_AUDIO, path])
#    #om ingen app:
#    subprocess.run(['open', path])
#
#
#    if APP_PDF:
#        subprocess.run(['open', '-a', APP_PDF, path])
#    else:
#        subprocess.run(['open', path])
#
#
#
#
