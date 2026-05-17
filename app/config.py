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
PATH_BACKUP, PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, PATH_HTML = None, None, None, None, None
SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_PASSWORD, SFTP_KEY, SFTP_REMOTE_PATH = None, None, None, None, None, None

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
        "html": "html"
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
        "password": "",
        "key_file": "",
        "remote_path": ""
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
        define_apps()  # Define default apps
        define_sftp()  # Define settings for sftp connection
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
    global DB_FILE, BASE_DIR, PATH_DATABASE, PATH_BACKUP, ARCHIVE_ROOT, PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, PATH_HTML
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

    PATH_DATABASE.mkdir(parents=True, exist_ok=True)  # Make sure these directories exist
    PATH_BACKUP.mkdir(parents=True, exist_ok=True)
    PATH_MANUSCRIPTS.mkdir(parents=True, exist_ok=True)
    PATH_RECORDINGS.mkdir(parents=True, exist_ok=True)
    PATH_RESOURCES.mkdir(parents=True, exist_ok=True)
    PATH_HTML.mkdir(parents=True, exist_ok=True)

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
    global SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_PASSWORD, SFTP_KEY, SFTP_REMOTE_PATH
    if not CONFIG:
        load_config()
    sftp_config = CONFIG.get('sftp', {})
    SFTP_HOST = sftp_config.get('host')
    SFTP_PORT = sftp_config.get('port', 22)
    SFTP_USER = sftp_config.get('username')
    SFTP_PASSWORD = sftp_config.get('password')
    SFTP_KEY = sftp_config.get('key_file')
    SFTP_REMOTE_PATH = sftp_config.get('remote_path')

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




