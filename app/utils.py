from pathlib import Path
#import shutil
import sqlite3
from app.config import DB_FILE, PATH_BACKUP
from datetime import datetime, date, timedelta
import re
from app.presentation.common import ICON, console


PATTERN = {}  # Patterns to check validity of user inputs when creating and editing a sermon
PATTERN['code'] = re.compile(r'^P\d{3}$')  # Sermon code on this format: P372 etc
PATTERN['related_sermons'] = re.compile(r'^P\d{3}((\s*\,\s*)(P\d{3}))*$') # P001, P002 etc
PATTERN['date'] = re.compile(r'^20\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[0-1])$') # Date: YYYY-MM-DD, does not validate dates
PATTERN['manuscript'] = re.compile(r'^P\d{3}[abcde]?\.(pdf|PDF)$')  # Manuscript P371.pdf, P371b.PDF
PATTERN['recording'] = re.compile(r'^20\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[0-1])_Predikan.*\..{3}$')  # Recording 2026-01-25_Predikan.mp3 but also 2026-01-25_Predikan_2.mp4 and others variants
PATTERN['file_name'] = re.compile(r'^.+\..{3}$')  # Generic file name
PATTERN['url'] = re.compile(r'^https?\:\/\/')  # URL http(s)://...



def get_last_sunday():
    """Gets date of the last Sunday (including today)."""
    today = date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    last_sunday = today - timedelta(days=days_since_sunday)
    return last_sunday.isoformat()  


def get_file_link(path, file_name, title = None, show_missing_file = True, show_title_if_missing = True):
    """Get a link to path/file with styles for print in console"""
    if not title:
        title = file_name
    if 'http' in file_name:  # Probably not a file but an URL
        return f"[link={file_name}]{title}[/link]"
    if not file_name:
        return ''
    file_path = path / Path(file_name)
    marker = ''
    if show_missing_file:
        if not file_path.is_file():  # File does not exist
            marker = f"[alert]{ICON['missing_file']}[/alert]"  # Mark missing file with an icon and style
            if show_title_if_missing:  # Show marker next to title or only marker?
                return f"{marker} [link=file://{file_path}]{title}[/link]"  # ✘ P371.pdf
            else:
                return f"[link=file://{file_path}]{marker}[/link]"  # ✘
    return f"[link=file://{file_path}]{title}[/link]"


def backup_database():
    """Save a copy of the database file under new name."""

    try:
        backup_dir = PATH_BACKUP
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d")
        backup_file = backup_dir / f"sermon_{timestamp}.db"

        #shutil.copy2(DB_FILE, backup_file)

        with sqlite3.connect(DB_FILE) as source:
            with sqlite3.connect(backup_file) as target:
                source.backup(target)

        return backup_file
    except Exception:
        raise DatabaseError('Fel vid säkerhetskopiering av databasen')


