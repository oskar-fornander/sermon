#app/services/open.py
import subprocess
from app.utils import parse_sermon_code
from app.presentation.common import clear_screen
from app.config import APP_PDF, APP_AUDIO, APP_VIDEO, APP_URL


def open_manuscript(sermon_code: str):
    """Open manuscript for sermon"""
    console.print(f"Öppna manus till predikan {sermon_code}")
    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format



def open_recording(sermon_code: str):
    """Open recording for sermon"""
    console.print(f"Öppna inspelning till predikan {sermon_code}")
    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format



def open_resource(sermon_code: str):
    """Open resource for sermon"""
    console.print(f"Öppna resurs till predikan {sermon_code}")
    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format




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
