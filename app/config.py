# app/config.py

import sys
from pathlib import Path
import yaml
import sqlite3
from app.presentation.common import console


CONFIG_DIR = Path.home() / ".config" / "sermon"  # This is the absolute path to config.yaml
CONFIG_FILE = CONFIG_DIR / "config.yaml"

CONFIG = None
ARCHIVE_ROOT, PATH_DATABASE, DB_FILE  = None, None, None
PATH_BACKUP, PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, PATH_HTML = None, None, None, None, None

DEFAULT_CONFIG = {
    "root": str(Path.home() / "predikan" / "archive"),
    "database": "sermon.db",
    "paths": {
        "database": "data",
        "backup": "data/backup",
        "manuscripts": "files/manuscripts",
        "recordings": "files/recordings",
        "resources": "files/resources",
        "html": "html"
    }
}

def init_environment():
    """Initialize the environment"""
    load_config()  # Load config.yaml

    try:
        define_paths()  # Define paths for all files and folders
    except Exception as error:
        console.print(error)
        console.print('Programmet avslutas.')
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




def ensure_database():
    """Create database file if non-existing"""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    create_schema(conn)
    conn.close()


def create_schema(conn):
    schema_path = Path(__file__).parent.parent / 'schema.sql'
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()




