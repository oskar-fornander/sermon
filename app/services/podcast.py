#app/services/podcast.py

from dataclasses import dataclass
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from jinja2 import Environment, FileSystemLoader
from app.errors import NotFoundError, FileError
from app.utils import parse_sermon_code, PATTERN, rss_date
from app.config import USER, PATH_RECORDINGS, PATH_PODCAST, PODCAST_FEED, PODCAST_AUDIO, PODCAST_COVER, PODCAST_TITLE, PODCAST_DESCRIPTION, PODCAST_AUTHOR, PODCAST_MAX_DAYS
from app.services.sermon_draft import load_sermon_as_draft
from app.presentation.common import console, user_input, clear_screen


LOCAL_FEED = PATH_PODCAST / PODCAST_FEED[PODCAST_FEED.rfind('/') + 1:]  # Local path to feed.xml


# Special data class for a podcast episode
@dataclass
class Episode:
    title: str
    description: str
    pub_date: str
    url: str
    size: int
    path: Path | None = None

    @classmethod
    def from_xml(cls, item):
        enclosure = item.find('enclosure')
        return cls(
            title=item.findtext('title', ''),
            description=item.findtext('description', ''),
            pub_date=item.findtext('pubDate', ''),
            url=enclosure.get('url', ''),
            size=int(enclosure.get('length', 0))
        )

def load_episodes_from_xml(feed_file: Path = LOCAL_FEED) -> list[Episode]:
    tree = ET.parse(feed_file)
    root = tree.getroot()

    episodes = [
        Episode.from_xml(item)
        for item in root.findall("./channel/item")
    ]

    return episodes



def publish_episode(data: str):
    """Publish an episode to the podcast."""
    clear_screen()

    # 1. Prepare episode object to publish
    # 2. update local feed.xml
    #       - Read from local feed.xml
    #       - Extract all items
    #       - Remove items that shall not remain
    #       - Add new item
    #       - Sort
    #       - Render a new feed.xml
    #       - Save locally
    # 3. upload mp3
    # 4. upload feed.xml



    # 1. Determine if data is a sermon code or external file and build an episode object to publish
    file = Path(data).expanduser().resolve()  # Get absolute path if data is a filename, relative or absolute path
    console.print(file)

    code = re.compile(r'^[Pp]?\d{3}$')  # Sermon code on this format: P372 etc
    if code.match(data):
        episode = episode_from_sermon(data)
    elif '.' in data:  # Probably a file name
        if not file.is_file():
            raise FileError(f"Filen {file} hittades inte.")
        episode = episode_from_file(data)
    else:
        raise NotFoundError(f"'{data}' är varken en existerande fil eller en giltig predikokod.")
    console.print(episode)


    # 2. Update feed.xml by adding the new episode
    episodes = load_episodes_from_xml()  # Load all episodes from local feed.xml
    console.print(episodes)

    # episode ...





def episode_from_sermon(sermon_code: str) -> Episode:
    """Make episode object from sermon in database."""

    sermon_code = parse_sermon_code(sermon_code)  # Make sure code is in correct format or raise error
    sermon_draft = load_sermon_as_draft(sermon_code)
    #console.print(sermon_draft)

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
    time = '10:00'  # Default time
    pub_date = rss_date(date, time)

    file_name = recording.file_name
    if file_name[-4:] != '.mp3':
        raise FileError(f"Fel format på inspelning: {file_name} (ska vara .mp3)")

    place = ''
    for service in sermon_draft.services:
        if service.date == date:
            place = service.place

    mp3_path = PATH_RECORDINGS / file_name
    if not mp3_path.is_file():
        raise FileError(f"Filen {mp3_path} saknas.")
    size = Path(mp3_path).stat().st_size

    # Make an episode object
    episode = Episode(
        title=f"Predikan: {sermon_draft.title} | {USER}, {date}",
        description=f"{sermon_draft.introduction} | {place}, {date}",
        pub_date=pub_date,
        url=f"{PODCAST_AUDIO}/{file_name}",
        size=size,
        path=mp3_path)

    return episode



def episode_from_file(file_name: str) -> Episode:
    """Make episode object from external file and user input."""

    path = Path(file_name).expanduser().resolve()  # Get absolute path if data is a filename, relative or absolute path
    size = Path(path).stat().st_size

    # User input
    title = user_input('Avsnittets titel', allow_empty=False)
    description = user_input('Beskrivning av avsnittet', allow_empty=True)
    date = user_input('Datum för publicering', ' [ÅÅÅÅ-MM-DD]', pattern=PATTERN['date'], allow_empty=False)
    time = user_input('Klockslag för publicering', ' [HH:MM]', default='10:00', pattern=PATTERN['time'], allow_empty=False)
    pub_date = rss_date(date, time)


    # Make an episode object
    episode = Episode(
        title=title,
        description=description,
        pub_date=pub_date,
        url=f"{PODCAST_AUDIO}/{file_name}",
        size=size,
        path=path)

    return episode


