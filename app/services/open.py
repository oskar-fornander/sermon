#app/services/open.py
import subprocess
from pathlib import Path
import requests
from app.utils import parse_sermon_code
from app.presentation.common import clear_screen, console, user_choice
from app.config import APP_PDF, APP_AUDIO, APP_VIDEO, APP_URL, PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from app.db import get_manuscripts_for_sermon, get_recordings_for_sermon, get_resources_for_sermon
from app.errors import FileError, ValidationError



def open_manuscript(sermon_code: str):
    """Open manuscript for sermon"""
    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format
    console.print(f"Öppna manus till predikan {sermon_code}")

    manuscripts = get_manuscripts_for_sermon(sermon_code)
    
    if not manuscripts:
        raise FileError(f"Det finns inget manus till predikan {sermon_code}.")

    i = 1
    if len(manuscripts) > 1:
        txt = ''
        for i, m in enumerate(manuscripts):
            txt += f"\n[key]{i + 1}.[/key] [title]{m['file_name']}[/title], {m['date']} "
            if m['notes']:
                txt += f"[notes]({m['notes']})[/notes]"
        console.print(txt + '\n[key]q.[/key] [title]Avbryt[/title]\n')
        i =  user_choice(title='Välj manus att öppna', options=[str(i) for i in range(1, len(manuscripts) + 1)] + ['q'])
        if i == 'q':
            return
    
    file_name = manuscripts[int(i) - 1]['file_name']
    path = PATH_MANUSCRIPTS / file_name

    if not Path.is_file(path):
        raise FileError(f"Filen [link_style][link=file://{PATH_MANUSCRIPTS}]{PATH_MANUSCRIPTS}[/link]/{file_name}[/link_style] saknas.")


    try:
        if APP_PDF:
            console.print(f"Öppnar [link=file://{path}]{file_name}[/link] med {APP_PDF} ...")
            subprocess.run(['open', '-a', APP_PDF, path])
        else:
            console.print(f"Öppnar [link=file://{path}]{file_name}[/link] ...")
            subprocess.run(['open', path])
    except Exception:
        raise FileError(f"Det gick inte att öppna filen {path}")


def open_recording(sermon_code: str):
    """Open recording for sermon"""
    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format
    console.print(f"Öppna inspelning till predikan {sermon_code}")

    recordings = get_recordings_for_sermon(sermon_code)

    if not recordings:
        raise FileError(f"Det finns ingen inspelning till predikan {sermon_code}.")

    i = 1
    if len(recordings) > 1:
        txt = ''
        for i, r in enumerate(recordings):
            link = r['file_name'] or r['external_url']
            txt += f"\n[key]{i + 1}.[/key] [title]{r['date']}[/title] {link} ({r['type']}) "
            if r['notes']:
                txt += f"[notes]({r['notes']})[/notes]"
        console.print(txt + '\n[key]q.[/key] [title]Avbryt[/title]\n')
        i =  user_choice(title='Välj inspelning att öppna', options=[str(i) for i in range(1, len(recordings) + 1)] + ['q'])
        if i == 'q':
            return
    
    recording = recordings[int(i) - 1]
    file_name = recording['file_name']
    external_url = recording['external_url']

    if file_name:  # Open file
        path = PATH_RECORDINGS / file_name

        if not Path.is_file(path):
            raise FileError(f"Filen [link_style][link=file://{PATH_RECORDINGS}]{PATH_RECORDINGS}[/link]/{file_name}[/link_style] saknas.")

        if recording['type'] == 'audio':
            APP = APP_AUDIO
        elif recording['type'] == 'video':
            APP = APP_VIDEO
        else:
            raise FileError('Inte angiven filtyp: audio eller video')

        try:
            if APP:
                console.print(f"Öppnar [link=file://{path}]{file_name}[/link] med {APP} ...")
                subprocess.run(['open', '-a', APP, path])
            else:
                console.print(f"Öppnar [link=file://{path}]{file_name}[/link] ...")
                subprocess.run(['open', path])
        except Exception:
            raise FileError(f"Det gick inte att öppna filen {path}")

    elif external_url:  # Open external url
        if not url_is_ok(external_url):
            raise ValidationError(f"Länken verkar vara trasig: [link={external_url}]{external_url}[/link]")
        try:
            if APP_URL:
                console.print(f"Öppnar [link={external_url}]{external_url}[/link] med {APP_URL} ...")
                subprocess.run(['open', '-a', APP_URL, external_url])
            else:
                console.print(f"Öppnar [link={external_url}]{file_name}[/link] ...")
                subprocess.run(['open', external_url])
        except Exception:
            raise FileError(f"Det gick inte att öppna länken {external_url}")

    else:
        raise FileError('Ingen fil eller extern url finns.')



def open_resource(sermon_code: str):
    """Open resource for sermon"""
    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format
    console.print(f"Öppna resurs till predikan {sermon_code}")

    resources = get_resources_for_sermon(sermon_code)

    if not resources:
        raise FileError(f"Det finns ingen resurs till predikan {sermon_code}.")

    i = 1
    if len(resources) > 1:
        txt = ''
        for i, r in enumerate(resources):
            txt += f"\n[key]{i + 1}.[/key] [title]{r['title']}[/title] ({r['file_name']}) "
            if r['notes']:
                txt += f"[notes]({r['notes']})[/notes]"
        console.print(txt + '\n[key]q.[/key] [title]Avbryt[/title]\n')
        i =  user_choice(title='Välj resurs att öppna', options=[str(i) for i in range(1, len(resources) + 1)] + ['q'])
        if i == 'q':
            return
    
    file_name = resources[int(i) - 1]['file_name']
    path = PATH_RESOURCES / file_name

    if not Path.is_file(path):
        raise FileError(f"Filen [link_style][link=file://{PATH_RESOURCES}]{PATH_RESOURCES}[/link]/{file_name}[/link_style] saknas.")

    try:
        if APP_PDF:
            console.print(f"Öppnar [link=file://{path}]{file_name}[/link] med {APP_PDF} ...")
            subprocess.run(['open', '-a', APP_PDF, path])
        else:
            console.print(f"Öppnar [link=file://{path}]{file_name}[/link] ...")
            subprocess.run(['open', path])
    except Exception:
        raise FileError(f"Det gick inte att öppna filen {path}")



def url_is_ok(url: str) -> bool:
    try:
        r = requests.head(url, allow_redirects=True, timeout=3)
        return r.status_code < 400
    except requests.RequestException:
        return False



