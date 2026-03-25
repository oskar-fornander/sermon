from pathlib import Path
from urllib import parse
from mutagen.mp3 import MP3
from pypdf import PdfReader
#import shutil
import sqlite3
from app.config import DB_FILE, PATH_BACKUP
from datetime import datetime, date, timedelta
import re
from app.presentation.common import ICON, console
from app.errors import ValidationError


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

def parse_month(value: str) -> int:
    MONTH_MAP = {
        "1": 1, "01": 1, "jan": 1, "januari": 1, "january": 1,
        "2": 2, "02": 2, "feb": 2, "febr": 2, "februari": 2, "february": 2,
        "3": 3, "03": 3, "mar": 3, "mars": 3, "march": 3,
        "4": 4, "04": 4, "apr": 4, "april": 4,
        "5": 5, "05": 5, "maj": 5, "may": 5,
        "6": 6, "06": 6, "jun": 6, "juni": 6, "june": 6,
        "7": 7, "07": 7, "jul": 7, "juli": 7, "july": 7,
        "8": 8, "08": 8, "aug": 8, "augusti": 8, "august": 8,
        "9": 9, "09": 9, "sep": 9, "sept": 9, "september": 9,
        "10": 10, "okt": 10, "oktober": 10, "october": 10,
        "11": 11, "nov": 11, "november": 11,
        "12": 12, "dec": 12, "december": 12,
    }
    if not value:
        return None
    key = value.strip().lower()
    if key not in MONTH_MAP:
        raise ValidationError(f"Ogiltig månad: {value}")
    return MONTH_MAP[key]


def get_file_link(path, file_name, title = None, show_missing_file = True, show_title_if_missing = True, show_meta = False):
    """Get a link to path/file with styles for print in console"""
    if not title:
        title = file_name
    if 'http' in file_name:  # Probably not a file but an URL
        return f"[link={file_name}]{title}[/link]"
    if not file_name:
        return ''
    file_path = path / Path(file_name.strip())
    url_encoded_path = parse.quote(file_path.as_posix())  # This takes care of special characters and spaces in file names
    marker = ''
    if show_missing_file:
        if not file_path.is_file():  # File does not exist
            marker = f"[alert]{ICON['missing_file']}[/alert]"  # Mark missing file with an icon and style
            if show_title_if_missing:  # Show marker next to title or only marker?
                return f"{marker} [link=file://{url_encoded_path}]{title}[/link]"  # ✘ P371.pdf
            else:
                return f"[link=file://{url_encoded_path}]{marker}[/link]"  # ✘
    if show_meta:  # Show length of mp3-file and number of pages in pdf
        meta = ''
        if '.mp3' in file_name:
            meta = f" [notes]({get_audio_length(url_encoded_path)})[/notes]"
        elif '.pdf' in file_name:
            meta = f" [notes]({get_pdf_pages(url_encoded_path)})[/notes]"
        return f"[link=file://{url_encoded_path}]{title}[/link]{meta}"
    return f"[link=file://{url_encoded_path}]{title}[/link]"


def get_audio_length(path: str) -> str:
    """Get length of an mp3 audio file in minutes and seconds"""
    try:
        audio = MP3(path)
        length_seconds = int(audio.info.length)
        m, s = divmod(length_seconds, 60)
        return f"{m}:{s:02}"
    except Exception:
        return ''

def get_pdf_pages(path: str) -> str:
    """Get number of pages in a pdf document"""
    try:
        reader = PdfReader(path)
        num_pages = len(reader.pages)
        if num_pages < 2:
            return f"{num_pages} sida"
        return f"{num_pages} sidor"
    except Exception:
        return ''


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


