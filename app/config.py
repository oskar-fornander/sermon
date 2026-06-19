# app/config.py

import sys
from pathlib import Path
import yaml
import sqlite3
import logging
from app.presentation.common import console, user_confirmation
from app.errors import DatabaseError


CONFIG_DIR = Path.home() / ".config" / "sermon"  # This is the absolute path to config.yaml
CONFIG_FILE = CONFIG_DIR / "config.yaml"

CONFIG = None
USER = ''
ARCHIVE_ROOT, PATH_DATABASE, DB_FILE  = None, None, None
PATH_BACKUP, PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, PATH_HTML, PATH_PODCAST = None, None, None, None, None, None
CLOUD_PROVIDER, CLOUD_MANUSCRIPTS, CLOUD_RECORDINGS, CLOUD_RESOURCES = None, None, None, None 
SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_KEY  = None, None, None, None
WEB_URL, WEB_ROOT, HTML_REMOTE_DIR = None, None, None
PODCAST_REMOTE_DIR, PODCAST_FEED, LOCAL_PODCAST_FEED, PODCAST_AUDIO, PODCAST_COVER, PODCAST_TITLE, PODCAST_DESCRIPTION, PODCAST_AUTHOR, PODCAST_MIN_EPISODES, PODCAST_MAX_DAYS = None, None, None, None, None, None, None, None, None, None
APP_PDF, APP_AUDIO, APP_VIDEO, APP_URL = None, None, None, None

HAS_CLOUD, HAS_SFTP, HAS_HTML, HAS_PODCAST = None, None, None, None  # Feature flags


DEFAULT_CONFIG = {
    "user": "",
    "archive_path": str(Path.home() / "predikan" / "archive"),
    "cloud": {
        "provider": "",
        "urls": {
            "manuscripts": "",
            "recordings": "",
            "resources": ""
        }
    },
    "apps": {
        "pdf": "",
        "audio": "",
        "video": "",
        "browser": ""
    },
    "web": {
        "url": ""
    },
    "sftp": {
        "root": "",
        "host": "",
        "port": "",
        "username": "",
        "key_file": ""
    },
    "html": {
        "remote_dir": ""
    },
    "podcast": {
        "remote_dir": "",
        "cover_image": "",
        "title": "",
        "description": "",
        "author": "",
        "min_episodes": 3,
        "max_days": 60
    }
}

logging.getLogger('pypdf').setLevel(logging.ERROR)  # Hide non critical error messages

def get_user():
    load_config()
    user = CONFIG.get('user') or ''
    return user

def init_environment():
    """Initialize the environment"""
    global USER, HAS_CLOUD, HAS_SFTP, HAS_HTML, HAS_PODCAST
    load_config()  # Load config.yaml
    if not CONFIG:
        raise RuntimeError(f"Fel vid inläsning av konfigurationsfilen {CONFIG_FILE}")

    try:
        USER = CONFIG.get('user') or ''
        define_paths()  # Define paths for all files and folders
        define_cloud()  # Define paths for cloud service (used in exported html file)
        HAS_CLOUD = CLOUD_PROVIDER and CLOUD_MANUSCRIPTS and CLOUD_RECORDINGS and CLOUD_RESOURCES  # Set feature flag for cloud service
        define_apps()  # Define default apps
        define_sftp()  # Define settings for sftp connection
        HAS_SFTP = SFTP_HOST and SFTP_PORT and SFTP_USER and SFTP_KEY and WEB_URL
        HAS_HTML = HTML_REMOTE_DIR != ''
        define_podcast()  # Define settings and paths for podcast
        HAS_PODCAST = PODCAST_REMOTE_DIR and PODCAST_TITLE
    except Exception as error:
        raise RuntimeError(f"Ett fel uppstod i uppstarten: {error}")

    ensure_database()  # Create database file if it does not exist



def ensure_config_exists():
    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            yaml.safe_dump(DEFAULT_CONFIG, f, sort_keys=False)

        console.print(f"Ny konfigurationsfil skapad: {CONFIG_FILE} \nRedigera den för att ange korrekt sökväg till predikoarkivet och övriga inställningar. \nProgrammet avslutas.")
        sys.exit(1)  # Quit


def get_added_keys(default, user, prefix=""):
    """Find keys present in default but missing in user."""
    added = []
    if not isinstance(user, dict):
        user = {}
    for key, val in default.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if key not in user:
            added.append(full_key)
        elif isinstance(val, dict) and isinstance(user[key], dict):
            added.extend(get_added_keys(val, user[key], full_key))
    return added


def load_config():
    """Load config file"""
    global CONFIG
    ensure_config_exists()
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        loaded = yaml.safe_load(f)
    
    if loaded is None or not isinstance(loaded, dict):
        loaded = {}

    CONFIG = deep_merge(DEFAULT_CONFIG, loaded)  # Ensure all fields are present

    if CONFIG != loaded:
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                yaml.safe_dump(CONFIG, f, sort_keys=False)
            
            # Find the missing keys that were merged in
            added_keys = get_added_keys(DEFAULT_CONFIG, loaded)
            if added_keys:
                console.print(f"[info]Konfigurationsfilen {CONFIG_FILE} har uppdaterats med saknade inställningsfält: {', '.join(added_keys)}[/info]")
            
            if not CONFIG.get('user'):
                console.print("[info]Tips: Ange ditt namn under 'user' i konfigurationsfilen för att anpassa predikoarkivet.[/info]")
        except Exception as e:
            logging.warning(f"Kunde inte spara den uppdaterade konfigurationen: {e}")


def deep_merge(default, user):
    """Merge user config with default config."""
    if user is None:
        return default
    if not isinstance(user, dict):
        return default
    merged = default.copy()
    for key, value in user.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            if value is not None:  # Overwrite only if user has a value
                merged[key] = value
    return merged


def define_paths():
    """Define some file paths"""
    global DB_FILE, BASE_DIR, PATH_DATABASE, PATH_BACKUP, ARCHIVE_ROOT, PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, PATH_HTML, PATH_PODCAST
    if not CONFIG:
        load_config()

    ARCHIVE_ROOT = Path(CONFIG['archive_path']).expanduser().resolve()
    if not ARCHIVE_ROOT.exists():  # If the archive directory does not exist: quit and make sure to change in config or create it
        if user_confirmation(f"Konfigurerad arkivmapp för predikoarkivet finns inte: {ARCHIVE_ROOT}. Ska den skapas?", default=False):
            ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
            console.print(f"Mappen har skapats.")
        else:
            console.print(f"Ange korrekt sökväg under 'archive_path' i konfigurationsfilen: {CONFIG_FILE}")
            sys.exit(1)

    PATH_DATABASE = ARCHIVE_ROOT / 'data'
    DB_FILE = PATH_DATABASE / 'sermon.db'
    PATH_BACKUP = PATH_DATABASE / 'backup'
    PATH_MANUSCRIPTS = ARCHIVE_ROOT / 'files' / 'manuscripts'
    PATH_RECORDINGS = ARCHIVE_ROOT / 'files' / 'recordings'
    PATH_RESOURCES = ARCHIVE_ROOT / 'files' / 'resources'
    PATH_HTML = ARCHIVE_ROOT / 'html'
    PATH_PODCAST = ARCHIVE_ROOT / 'podcast'

    # Make sure these directories exist
    PATH_DATABASE.mkdir(parents=True, exist_ok=True)  
    PATH_BACKUP.mkdir(parents=True, exist_ok=True)
    PATH_MANUSCRIPTS.mkdir(parents=True, exist_ok=True)
    PATH_RECORDINGS.mkdir(parents=True, exist_ok=True)
    PATH_RESOURCES.mkdir(parents=True, exist_ok=True)
    PATH_HTML.mkdir(parents=True, exist_ok=True)
    PATH_PODCAST.mkdir(parents=True, exist_ok=True)


def define_cloud():
    """Define paths to cloud where files are saved"""
    global CLOUD_PROVIDER, CLOUD_MANUSCRIPTS, CLOUD_RECORDINGS, CLOUD_RESOURCES

    if not CONFIG:
        load_config()

    app_cloud = CONFIG.get('cloud', {})
    CLOUD_PROVIDER = app_cloud.get('provider', {})
    urls = app_cloud.get('urls', {})
    CLOUD_MANUSCRIPTS = urls.get('manuscripts') or ''
    CLOUD_RECORDINGS = urls.get('recordings') or ''
    CLOUD_RESOURCES = urls.get('resources') or ''


def define_apps():
    """Define default apps to use to open resources"""
    global APP_PDF, APP_AUDIO, APP_VIDEO, APP_URL
    if not CONFIG:
        load_config()
    app_config = CONFIG.get('apps', {})
    APP_PDF = app_config.get('pdf') or None
    APP_AUDIO = app_config.get('audio') or None
    APP_VIDEO = app_config.get('video') or None
    APP_URL = app_config.get('browser') or None

def define_sftp():
    """Define settings for sftp connection"""
    global SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_KEY, WEB_URL, WEB_ROOT, HTML_REMOTE_DIR
    if not CONFIG:
        load_config()
    sftp_config = CONFIG.get('sftp', {})
    SFTP_HOST = sftp_config.get('host') or None
    SFTP_PORT = str(sftp_config.get('port', 22))
    SFTP_USER = sftp_config.get('username') or None
    SFTP_KEY = sftp_config.get('key_file') or None

    WEB_URL = CONFIG.get('web', {}).get('url') or ''
    WEB_URL = WEB_URL.rstrip('/')
    WEB_ROOT = sftp_config.get('root') or ''
    WEB_ROOT = WEB_ROOT.rstrip('/')
    HTML_REMOTE_DIR = CONFIG.get('html', {}).get('remote_dir') or ''
    HTML_REMOTE_DIR = HTML_REMOTE_DIR.rstrip('/')


def define_podcast():
    """Define paths and settings for podcast"""
    global PODCAST_REMOTE_DIR, PODCAST_FEED, PODCAST_AUDIO, PODCAST_COVER, PODCAST_TITLE, PODCAST_DESCRIPTION, PODCAST_AUTHOR, PODCAST_MIN_EPISODES, PODCAST_MAX_DAYS, LOCAL_PODCAST_FEED
    if not CONFIG:
        load_config()
    podcast_config = CONFIG.get('podcast', {})

    PODCAST_REMOTE_DIR = podcast_config.get('remote_dir') or ''
    PODCAST_REMOTE_DIR = PODCAST_REMOTE_DIR.rstrip('/')
    PODCAST_FEED = 'feed.xml'
    LOCAL_PODCAST_FEED = PATH_PODCAST / PODCAST_FEED  # Local path to feed.xml
    PODCAST_AUDIO = f"{PODCAST_REMOTE_DIR}/audio"
    PODCAST_COVER = f"{PODCAST_REMOTE_DIR}/{podcast_config.get('cover_image') or ''}"

    PODCAST_TITLE = podcast_config.get('title') or ''
    PODCAST_DESCRIPTION = podcast_config.get('description') or ''
    PODCAST_AUTHOR = podcast_config.get('author') or ''

    PODCAST_MIN_EPISODES = int(podcast_config.get('min_episodes', '0'))
    PODCAST_MAX_DAYS = int(podcast_config.get('max_days', '365'))


def ensure_database():
    """Create database file if non-existing"""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("PRAGMA foreign_keys = ON")
        create_schema(conn)
        conn.close()
    except Exception:
        raise DatabaseError('Fel vid skapande av SQLite databasfil.')


def create_schema(conn):
    schema_path = Path(__file__).parent.parent / 'schema.sql'
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()


