from pathlib import Path
import yaml

CONFIG = None
BASE_DIR, DB_PATH, ARCHIVE_ROOT = None, None, None  


def load_config():
    """Load config file"""
    global CONFIG
    config_path = BASE_DIR / "config.yaml"
    with open(config_path, 'r') as f:
        CONFIG = yaml.safe_load(f)

def define_paths():
    """Define some file paths"""
    global BASE_DIR, CONFIG, DB_PATH, ARCHIVE_ROOT 
    BASE_DIR = Path(__file__).resolve().parent.parent
    if not CONFIG:
        load_config()

    DB_PATH = Path(CONFIG['database']['path'] + CONFIG['database']['filename'])
    ARCHIVE_ROOT = (BASE_DIR / CONFIG["archive"]["root"]).resolve()

