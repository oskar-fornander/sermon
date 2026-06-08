#app/services/podcast.py

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import re
from xml.etree import ElementTree as ET
from jinja2 import Environment, FileSystemLoader
from app.errors import NotFoundError, FileError
from app.utils import parse_sermon_code, PATTERN, rss_date, iso_date_from_rss_date, rss_date_days_old
from app.config import USER, WEB_URL, PATH_RECORDINGS, PATH_PODCAST, PODCAST_REMOTE_DIR, PODCAST_FEED, PODCAST_AUDIO, PODCAST_COVER, PODCAST_TITLE, PODCAST_DESCRIPTION, PODCAST_AUTHOR, PODCAST_MIN_EPISODES, PODCAST_MAX_DAYS
from app.services.sermon_draft import load_sermon_as_draft
from app.services.upload import upload_file, delete_file
from app.presentation.common import console, user_input, clear_screen, user_confirmation


LOCAL_FEED = PATH_PODCAST / PODCAST_FEED  # Local path to feed.xml


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


def list_episodes():
    """List all episodes in podcast feed."""
    pass


def publish_episode(data: str):
    """Publish an episode to the podcast."""

    # 1. Prepare episode object to publish
    # 2. update local feed.xml
    #       - Read from local feed.xml and extract all items
    #       - Add new item and sort
    #       - Render a new feed.xml
    #       - Save locally
    # 3. upload mp3
    # 4. upload feed.xml
    # 5. prune podcast



    # 1. Determine if data is a sermon code or external file and build an episode object to publish
    console.print('Hämtar data för podcast ...')
    file = Path(data).expanduser().resolve()  # Get absolute path if data is a filename, relative or absolute path

    code = re.compile(r'^[Pp]?\d{3}$')  # Sermon code on this format: P372 etc
    if code.match(data):
        episode = episode_from_sermon(data)
    elif '.' in data:  # Probably a file name
        if not file.is_file():
            raise FileError(f"Filen {file} hittades inte.")
        episode = episode_from_file(data)
    else:
        raise NotFoundError(f"'{data}' är varken en existerande fil eller en giltig predikokod.")
    #console.print(episode)
    if not episode:
        console.print("Inget avsnitt publicerat.")
        return

    if rss_date_days_old(episode.pub_date) > PODCAST_MAX_DAYS:  # Give a warning if uploading too old episode
        console.print(f"Detta avsnitt har ett publiceringsdatum som är äldre än {PODCAST_MAX_DAYS} dagar, som är maxgränsen för avsnitt angiven i konfigurationsfilen.")
        if not user_confirmation("Vill du ändå publicera avsnittet (under dagens datum)?", blank_line=False):
            console.print("Inget avsnitt publicerat.")
            return
        episode.pub_date = rss_date(datetime.today().date().isoformat()[:10])  # Set today as publication date for the uploaded episode

    # 2. Update feed.xml by adding the new episode
    episodes = load_episodes_from_xml()  # Load all episodes from local feed.xml
    dates = [e.pub_date for e in episodes]
    if episode.pub_date in dates:  # Is this episode already uploaded?
        title = episodes[dates.index(episode.pub_date)].title
        console.print(f"Det finns redan ett avsnitt med samma publiceringsdatum:\n[title]{title}[/title]")
        if not user_confirmation(f"Ska detta avsnitt ändå publiceras?", blank_line=False):
            console.print("Inget avsnitt publicerat.")
            return

    console.print(f"Uppdaterar {PODCAST_FEED} ...")
    episodes.append(episode)  # Add new episode
    episodes.sort(key=lambda x: iso_date_from_rss_date(x.pub_date), reverse=True)  # Sort all episodes by date in descending order
    list_episodes()
    render_podcast_feed(episodes)  # Render feed.xml and save locally

    # 3. Upload mp3
    console.print(f"Laddar upp fil: {episode.path.name} ...")
    upload_file(episode.path, episode.url)

    # 4. Upload feed.xml
    console.print(f"Laddar upp {PODCAST_FEED} ...")
    upload_file(LOCAL_FEED, PODCAST_REMOTE_DIR, PODCAST_FEED)

    # 5. Prune podcast
    prune_podcast() # Remove episodes older than PODCAST_MAX_DAYS if more than PODCAST_MIN_EPISODES episodes
    console.print('Klart.')


def prune_podcast():
    """Remove episodes older than PODCAST_MAX_DAYS if more than PODCAST_MIN_EPISODES episodes"""
    console.print('Raderar gamla avsnitt i podcast ...')
    to_remove = []
    episodes = load_episodes_from_xml()  # Load all episodes from local feed.xml
    episodes.sort(key=lambda x: iso_date_from_rss_date(x.pub_date), reverse=True)  # Sort all episodes by date
    while len(episodes) > PODCAST_MIN_EPISODES and rss_date_days_old(episodes[-1].pub_date) > PODCAST_MAX_DAYS:  # prune old episodes if more than minimum number of episodes currently in podcast and episode is older than maximum number of days
        to_remove.append(episodes.pop())

    if len(to_remove) == 0:
        console.print('Inga avsnitt att radera.')
        return
    for episode in to_remove:
        console.print(f"Raderar avsnitt: {iso_date_from_rss_date(episode.pub_date)[:10]}: {episode.title}")

    render_podcast_feed(episodes)  # Render feed.xml and save locally

    #upload feed.xml
    upload_file(LOCAL_FEED, PODCAST_REMOTE_DIR, PODCAST_FEED)
    console.print(f"Podcastens flöde är uppdaterat: [link={WEB_URL}/{PODCAST_REMOTE_DIR}/{PODCAST_FEED}]{WEB_URL}/{PODCAST_REMOTE_DIR}/{PODCAST_FEED}[/link]")

    #remove mp3 from server
    for episode in to_remove:
        delete_file(episode.url)



def render_podcast_feed(episodes):
    """Render feed.xml and save locally"""
    #console.print(episodes)

    # Build podcast feed.xml with Jinja2 template
    TEMPLATE_DIR = (Path(__file__).resolve().parent.parent / "templates")    
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('podcast.xml.j2')


    # One for local use:
    podcast_feed = template.render(
        title=PODCAST_TITLE,
        link=f"{WEB_URL}/{PODCAST_REMOTE_DIR}/{PODCAST_FEED}",
        description=PODCAST_DESCRIPTION,
        author=PODCAST_AUTHOR,
        cover=f"{WEB_URL}/{PODCAST_COVER}",
        episodes=episodes
    )

    file = PATH_PODCAST / PODCAST_FEED  # local feed.xml file
    with open(file, 'w', encoding='utf-8') as f:
        f.write(podcast_feed)

    #console.print(f"Export till [link=file://{file}]{PODCAST_FEED}[/link] är klart.")




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

    #console.print(recording)

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

    if user_confirmation(f"[sermon_code]{sermon_draft.code}[/sermon_code] [title]{sermon_draft.title}[/title], {date} {place}\nÄr detta predikan som ska publiceras i podcasten?", blank_line=False):
        return episode
    return None



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


    if user_confirmation(f"{episode.title}, {date} ({path.name})\nÄr detta det avsnitt som ska publiceras i podcasten?"):
        return episode
    return None



