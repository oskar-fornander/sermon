#app/services/podcast.py

from dataclasses import dataclass
#from typing import List
from jinja2 import Environment, FileSystemLoader
from app.errors import NotFoundError, FileError
from app.utils import parse_sermon_code
from app.config import USER, PODCAST_FEED, PODCAST_AUDIO, PODCAST_COVER, PODCAST_TITLE, PODCAST_DESCRIPTION, PODCAST_AUTHOR, PODCAST_MAX_DAYS
from app.services.sermon_draft import load_sermon_as_draft
from app.presentation.common import console, user_input


# Special data class for a podcast episode
@dataclass
class Episode:
    title: str
    description: str
    pub_date: str
    url: str
    size: int


def upload_sermon_to_podcast(sermon_code: str):
    """Export sermon to podcast."""

    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format or raise error
    sermon_draft = load_sermon_as_draft(sermon_code)
    console.print(sermon_draft)

    # There might be none or more than one recording ...
    recordings = sermon_draft.recordings
    recording = None
    if (len(recordings) == 0):
        raise NotFoundError(f"Predikan {sermon_code} har ingen inspelning.")
    elif (len(recordings) == 1):
        recording = recordings[0]
        if recording.type != 'audio' or not recording.file_name:
            raise NotFoundError(f"Predikan {sermon_code} har ingen inspelning.")
    elif (len(recordings) > 1):  # Select one of the recordings
        console.print(f"Predikan [sermon_code]{sermon_code}[/sermon_code] har flera inspelningar:")
        choices = []
        for i, recording in enumerate(recordings):
            if recording.type == 'audio' and recording.file_name:
                console.print(f"    {i + 1}. {recording.date} ({recording.type}) {recording.file_name}")
                choices.append(str(i + 1))
            else:
                console.print(f"[disabled]    {i + 1}. {recording.date} ({recording.type}) {recording.file_name or recording.external_url}[/disabled]")
        choice = user_input('Välj inspelning att publicera i podcasten', choices=choices)
        if not choice:
            console.print('Ingen inspelning vald. Inget publiceras.')
            return
        recording = recordings[int(choice) - 1]

    console.print(recording)

    date = recording.date  # Date for recording is also used to find service
    file_name = recording.file_name
    if file_name[-4:] != '.mp3':
        raise FileError(f"Fel format på inspelning: {file_name} (ska vara .mp3)")

    place = ''
    for service in sermon_draft.services:
        if service.date == date:
            place = service.place


    
    
    
# hämta path data från config ...

    






    episode = Episode(
        title=f"Predikan: {sermon_draft.title} | {USER}, {date}",
        description=f"{sermon_draft.introduction} | {place}, {date}",
        pub_date=date,
        url=f"{PODCAST_AUDIO}/{file_name}",
        size=0
            )



def upload_item_to_podcast():
    pass
    

def upload_podcast_episode():





# 1. uppdatera lokal feed.xml
#       . Läs befintlig feed.xml
#       . Extrahera alla items
#       . Rensa bort sådant som ska bort
#       . Lägg till nytt item
#       . Sortera
#       . Rendera om hela feed.xml med Jinja
#       . sparar den lokalt
# 2. ladda upp mp3
# 3. ladda upp feed.xml



    console.print('TODO: Skriv kod för att exportera som podcast.')





