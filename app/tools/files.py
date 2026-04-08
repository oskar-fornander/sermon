from pathlib import Path
import unicodedata
from app.config import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from app.db import get_all_manuscripts, get_all_recordings, get_all_resources
from app.errors import *
from app.presentation.common import console, clear_screen, render_info_panel
from app.utils import get_file_link


def normalize_filename(s: str) -> str:
    #return unicodedata.normalize("NFC", s).strip()
    return unicodedata.normalize("NFC", s).strip().replace('\xa0', ' ')

def check_files():
    """Check files associated with the sermons in the database: unused and missing files."""


    for file_type, func, path in (('manus', get_all_manuscripts, PATH_MANUSCRIPTS), ('inspelningar', get_all_recordings, PATH_RECORDINGS), ('resurser', get_all_resources, PATH_RESOURCES)):
        rows = func()  # Get all manuscripts/recordings/resources from database
        #print([row['file_name'] for row in rows])
        codes_by_filenames = {normalize_filename(file): code for file, code in rows}
        db_files = {normalize_filename(file) for file, code in rows}
        disk_files = list_files(path)

        #console.print(db_files)
        #console.print(disk_files)

        missing_files = db_files - disk_files
        unused_files = disk_files - db_files
        unused_files = [f for f in unused_files if f[0] != '.']  # Ignore hidden files (starting with a dot)

        missing_files = [f"[key]{codes_by_filenames[x]}:[/key] {x}" for x in missing_files]
        missing_files.sort()
        unused_files = [get_file_link(path, x, show_missing_file=False) for x in unused_files]
        unused_files.sort()

        render_info_panel(f"{file_type.upper()}: Saknade filer", '; '.join(missing_files))
        render_info_panel(f"{file_type.upper()}: Oanvända filer", '; '.join(unused_files))



def list_files(path: Path):

    return {normalize_filename(p.name) for p in path.iterdir() if p.is_file()}






