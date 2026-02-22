import yaml
from pathlib import Path
from dataclasses import asdict
from send2trash import send2trash
from datetime import datetime
from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from app.db import delete_sermon_from_database, load_sermon_as_draft
from app.presentation.common import console, clear_screen, render_info_panel, user_input, user_confirmation, user_choice



# Delete sermon from database

def delete_sermon(sermon_code: str):
    """Delete sermon"""

    # Double user confirmations before deleting
    if user_confirmation(f"Predikan [key]{sermon_code}[/key] och alla tillhörande filer kommer att raderas. Är du säker på att du vill fortsätta?", default = False):
        if user_confirmation(f"Denna åtgärd går inte att ångra; all data för [key]{sermon_code}[/key] kommer att försvinna. Radera?", default = False):
            draft = load_sermon_as_draft(sermon_code)
            sermon_id = draft.id  # internal database id for this sermon

            # 1. Save sermon draft temporarily in a file and erase it
            trash_dir = Path.home() / ".sermon_cli" / "trash"
            trash_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{draft.code}_{timestamp}.yaml"
            file_path = trash_dir / filename

            with open(file_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(
                    asdict(draft),
                    f,
                    allow_unicode=True,
                    sort_keys=False
                )

            send2trash(str(file_path))  # Erase sermon draft yaml-file

            # 2. Delete files connected to this sermon
            files = []
            for manuscript in draft.manuscripts:
                files.append(f"{PATH_MANUSCRIPTS}/{manuscript.file_name}")
            for recording in draft.recordings:
                files.append(f"{PATH_RECORDINGS}/{recording.file_name}")
            for resource in draft.resources:
                files.append(f"{PATH_RESOURCES}/{resource.file_name}")
            #console.print(f"Följande filer raderas: {', '.join([f[f.rfind('/') + 1:] for f in files])}")
            for file in files:
                try:
                    send2trash(file)
                    console.print(f"Filen {file[file.rfind('/') + 1:]} raderad.")
                except:
                    console.print(f"Filen {file[file.rfind('/') + 1:]} finns inte.")

            # 3. Delete sermon from database
            delete_sermon_from_database(sermon_id)

            console.print(f"Predikan [key]{sermon_code}[/key] och alla tillhörande filer är raderade.")
            
            return
    console.print(f"Predikan [key]{sermon_code}[/key] har [italic]inte[/italic] raderats.")




class PendingFileDeletions:
    def __init__(self):
        self._paths = []

    def add(self, path: Path):
        self._paths.append(path)

    def execute(self):
        files_deleted = []
        files_not_deleted = []
        from send2trash import send2trash
        for path in self._paths:
            if path.exists():
                send2trash(str(path))
                console.print(f"Fil raderad: {str(path)[str(path).rfind('/') + 1:]}")
            else:
                console.print(f"Fil existerar inte: {str(path)[str(path).rfind('/') + 1:]}")


    def clear(self):
        self._paths.clear()



