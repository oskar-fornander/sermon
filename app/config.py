# app/config.py

import sys
from pathlib import Path
import yaml
import sqlite3
import logging
from app.presentation.common import console


CONFIG_DIR = Path.home() / ".config" / "sermon"  # This is the absolute path to config.yaml
CONFIG_FILE = CONFIG_DIR / "config.yaml"

CONFIG = None
USER = ''
ARCHIVE_ROOT, PATH_DATABASE, DB_FILE  = None, None, None
PATH_BACKUP, PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, PATH_HTML, PATH_PODCAST = None, None, None, None, None, None
CLOUD_PROVIDER, CLOUD_MANUSCRIPTS, CLOUD_RECORDINGS, CLOUD_RESOURCES = None, None, None, None 
SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_KEY, SFTP_REMOTE_PATH, SFTP_URL = None, None, None, None, None, None
PODCAST_FEED, PODCAST_AUDIO, PODCAST_COVER, PODCAST_TITLE, PODCAST_DESCRIPTION, PODCAST_AUTHOR, PODCAST_MAX_DAYS = None, None, None, None, None, None, None 

APP_PDF, APP_AUDIO, APP_VIDEO, APP_URL = None, None, None, None


DEFAULT_CONFIG = {
    "user": "",
    "root": str(Path.home() / "predikan" / "archive"),
    "database": "sermon.db",
    "paths": {
        "database": "data",
        "backup": "data/backup",
        "manuscripts": "files/manuscripts",
        "recordings": "files/recordings",
        "resources": "files/resources",
        "html": "html",
        "podcast": "podcast"
    },
    "cloud": {
        "provider": "",
        "urls": {
            "manuscripts": "",
            "recordings": "",
            "resources": ""
        }
    },
    "apps": {
        "pdf": "Preview",
        "audio": "QuickTime Player",
        "video": "QuickTime Player",
        "browser": "Safari"
    },
    "sftp": {
        "host": "",
        "port": "",
        "username": "",
        "key_file": "",
        "remote_path": "",
        "public_url": ""
    },
    "podcast": {
        "base_url": "",
        "feed_path": "",
        "audio_path": "",
        "cover_image": "",
        "title": "",
        "description": "",
        "author": "",
        "max_days": "60"
    }
}


logging.getLogger('pypdf').setLevel(logging.ERROR)  # Hide non critical error messages

def get_user():
    init_environment()
    return USER

def init_environment():
    """Initialize the environment"""
    global USER
    load_config()  # Load config.yaml

    try:
        USER = CONFIG.get('user') or ''
        define_paths()  # Define paths for all files and folders
        define_cloud()  # Define paths for cloud service (used in exported html file)
        define_apps()  # Define default apps
        define_sftp()  # Define settings for sftp connection
        define_podcast()  # Define settings and paths for podcast
    except Exception as error:
        raise RuntimeError(f"Ett fel uppstod i uppstarten: {error}")
        sys.exit(1)

    ensure_database()  # Create database file if it does not exist



def ensure_config_exists():
    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            yaml.safe_dump(DEFAULT_CONFIG, f, sort_keys=False)

        console.print(f"Ny konfigurationsfil skapad: {CONFIG_FILE} \nRedigera den för att ange korrekt sökväg till predikoarkivet. \nProgrammet avslutas.")
        sys.exit(1)  # Quit


def load_config():
    """Load config file"""
    global CONFIG
    ensure_config_exists()
    with open(CONFIG_FILE, 'r') as f:
        CONFIG = yaml.safe_load(f)
    

def define_paths():
    """Define some file paths"""
    global DB_FILE, BASE_DIR, PATH_DATABASE, PATH_BACKUP, ARCHIVE_ROOT, PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, PATH_HTML, PATH_PODCAST
    if not CONFIG:
        load_config()

    ARCHIVE_ROOT = Path(CONFIG['root']).expanduser().resolve()
    if not ARCHIVE_ROOT.exists():  # If the root directory does not exist: quit and make sure to change in config or create it
        raise RuntimeError(
            f"Konfigurerad rotmapp finns inte: {ARCHIVE_ROOT}\n"
            f"Redigera {CONFIG_FILE} och ange korrekt sökväg och/eller skapa mappen."
        )

    PATH_DATABASE = ARCHIVE_ROOT / CONFIG['paths']['database']
    DB_FILE = PATH_DATABASE / CONFIG['database']
    PATH_BACKUP = ARCHIVE_ROOT / CONFIG['paths']['backup']
    PATH_MANUSCRIPTS = ARCHIVE_ROOT / CONFIG['paths']['manuscripts']
    PATH_RECORDINGS = ARCHIVE_ROOT / CONFIG['paths']['recordings']
    PATH_RESOURCES = ARCHIVE_ROOT / CONFIG['paths']['resources']
    PATH_HTML = ARCHIVE_ROOT / CONFIG['paths']['html']
    PATH_PODCAST = ARCHIVE_ROOT / CONFIG['paths']['podcast']

    PATH_DATABASE.mkdir(parents=True, exist_ok=True)  # Make sure these directories exist
    PATH_BACKUP.mkdir(parents=True, exist_ok=True)
    PATH_MANUSCRIPTS.mkdir(parents=True, exist_ok=True)
    PATH_RECORDINGS.mkdir(parents=True, exist_ok=True)
    PATH_RESOURCES.mkdir(parents=True, exist_ok=True)
    PATH_HTML.mkdir(parents=True, exist_ok=True)

def define_cloud():
    """Define paths to cloud where files are saved"""
    global CLOUD_PROVIDER, CLOUD_MANUSCRIPTS, CLOUD_RECORDINGS, CLOUD_RESOURCES

    if not CONFIG:
        load_config()

    app_cloud = CONFIG.get('cloud', {})
    CLOUD_PROVIDER = app_cloud.get('provider')
    urls = app_cloud.get('urls', {})
    CLOUD_MANUSCRIPTS = urls.get('manuscripts')
    CLOUD_RECORDINGS = urls.get('recordings')
    CLOUD_RESOURCES = urls.get('resources')


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
    global SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_KEY, SFTP_REMOTE_PATH, SFTP_URL
    if not CONFIG:
        load_config()
    sftp_config = CONFIG.get('sftp', {})
    SFTP_HOST = sftp_config.get('host')
    SFTP_PORT = str(sftp_config.get('port', 22))
    SFTP_USER = sftp_config.get('username')
    SFTP_KEY = sftp_config.get('key_file')
    SFTP_REMOTE_PATH = sftp_config.get('remote_path')
    SFTP_URL = sftp_config.get('public_url')

def define_podcast():
    """Define paths and settings for podcast"""
    global PODCAST_FEED, PODCAST_AUDIO, PODCAST_COVER, PODCAST_TITLE, PODCAST_DESCRIPTION, PODCAST_AUTHOR, PODCAST_MAX_DAYS
    if not CONFIG:
        load_config()
    podcast_config = CONFIG.get('podcast', {})
    podcast_url = podcast_config.get('base_url').rstrip('/')

    PODCAST_FEED = f"{podcast_url}/{podcast_config.get('feed_path').rstrip('/')}"
    PODCAST_AUDIO = f"{podcast_url}/{podcast_config.get('audio_path').rstrip('/')}"
    PODCAST_COVER = f"{podcast_url}/{podcast_config.get('cover_image')}"

    PODCAST_TITLE = podcast_config.get('title')
    PODCAST_DESCRIPTION = podcast_config.get('description')
    PODCAST_AUTHOR = podcast_config.get('author')

    PODCAST_MAX_DAYS = podcast_config.get('max_days')


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




