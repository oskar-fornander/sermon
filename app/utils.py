from pathlib import Path
from urllib import parse
from mutagen.mp3 import MP3
from pypdf import PdfReader
#import shutil
import sqlite3
from app.config import DB_FILE, PATH_BACKUP
from email.utils import format_datetime
from zoneinfo import ZoneInfo
from datetime import datetime, date, timedelta
import re
from app.presentation.common import ICON, console
from app.errors import ValidationError
from app.db import get_last_sermon_code

    #Convert date to correct format


PATTERN = {}  # Patterns to check validity of user inputs when creating and editing a sermon
PATTERN['code'] = re.compile(r'^P\d{3}$')  # Sermon code on this format: P372 etc
PATTERN['related_sermons'] = re.compile(r'^P\d{3}((\s*\,\s*)(P\d{3}))*$') # P001, P002 etc
PATTERN['date'] = re.compile(r'^20\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[0-1])$') # Date: YYYY-MM-DD, does not validate dates
PATTERN['time'] = re.compile(r'^[0-2]\d\:[0-5]\d$') # Time: HH:MM, does not validate time
PATTERN['iso_format'] = re.compile(r'^\d{4}-\d{2}-\d{2}$') # Date: YYYY-MM-DD, does not validate dates
PATTERN['manuscript'] = re.compile(r'^P\d{3}[abcde]?\.(pdf|PDF)$')  # Manuscript P371.pdf, P371b.PDF
PATTERN['recording'] = re.compile(r'^20\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[0-1])_Predikan.*\..{3}$')  # Recording 2026-01-25_Predikan.mp3 but also 2026-01-25_Predikan_2.mp4 and others variants
PATTERN['file_name'] = re.compile(r'^.+\..{3}$')  # Generic file name
PATTERN['url'] = re.compile(r'^https?\:\/\/')  # URL http(s)://...



def parse_sermon_code(code: str, raiseError = True) -> str:
    """Try parsing the input as a sermon code."""
    if PATTERN['code'].match(code):  # A valid code: P001
        return code
    for c in code:  # Invalid characters in code (spaces accepted)?
        if c not in 'Pp0123456789 ':
            if raiseError:
                raise ValidationError(f"Ange predikokod i korrekt format, t.ex. [key]{get_last_sermon_code()}[/key]")
            return None
    code = ''.join([c for c in code if c in '0123456789'])  # Extract only digits from code
    if code == '' or len(code) > 3:
        if raiseError:
            raise ValidationError(f"Ange predikokod i korrekt format, t.ex. [key]{get_last_sermon_code()}[/key]")
        return None
    code = 'P' + f"00{code}"[-3:]  # Padding zeros and leadning P
    return code



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


def validate_date(s):
    """Raises an error if date is not in ISO format."""
    if not PATTERN['iso_format'].match(s):
        raise ValidationError(f"Datum måste vara i formatet YYYY-MM-DD ({s})")
    try:
        datetime.strptime(s, '%Y-%m-%d')
    except Exception:
        raise ValidationError(f"Datum är ogiltigt ({s})")


def rss_date(date_str: str, time_str: str = '10:00') -> str:
    """Return date and time in format needed for podcast feed."""
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    dt = dt.replace(tzinfo=ZoneInfo("Europe/Stockholm"))
    return format_datetime(dt)

def iso_date_from_rss_date(date_str: str) -> str:
    """Return date in ISO format from rss date format."""
    date_str = date_str.strip()
    try:
        dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    except Exception:
        raise ValidationError(f"Ogiltigt RSS-datum: {date_str!r}")
    return dt.isoformat()[:19]  # Return date and time but remove time zone information (2026-05-24T10:00:00), this is sortable



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
        reader = PdfReader(path, strict=False)
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


