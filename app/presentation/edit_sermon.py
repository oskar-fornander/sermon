
from app.presentation.common import *
import os
import shutil
import tempfile
import subprocess
import time
from app.utils import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES, get_file_link


def render_edit_menu(title, options):
    """Show a menu for interactive editing"""

    menu = ''
    for i in range(len(options)):
        menu += f"[key]{i + 1}.[/key]{NBSP}{options[i]}  "

    subtitle = f"[bold][key]s[/key]: spara, [key]q[/key]: avbryt[/bold]"
    print()
    console.print(
        Panel(menu,
            title=f"[title]{title}[/title]",
            title_align='left', 
            subtitle=subtitle,
            subtitle_align='right',
            box=box.ROUNDED 
        )
    )
    print()


def find_fallback_editor() -> list[str] | None:
    for editor in ("nvim", "vim", "nano"):
        if shutil.which(editor):
            return [editor]
    return None

def user_edit_long_text(sermon_code, title, value):
    """Let user edit a long text with editor. Return edited text or None."""

    editor = os.environ.get("EDITOR")
    editor_cmd = None
    if editor:
        editor_cmd = editor.split()
    else:
        editor_cmd = find_fallback_editor()
    if not editor_cmd:
        raise RuntimeError('Ingen texteditor hittades (nvim/vim/nano)')

    console.print(f"[dim]Öppnar editor: {' '.join(editor_cmd)}[/dim]")
    time.sleep(1)

    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w+", delete=False) as tf:
        tf.write(value or '')
        tf.flush()
        path = tf.name

    try:
        subprocess.run(editor_cmd + [path], check=True)
        with open(path, 'r') as f:
            return f.read().strip() or None
    finally:
        os.unlink(path)



def user_edit_short_text_list(sermon_code, title, value):
    """Conver list to string before edit"""
    str = user_edit_short_text(title, '; '.join(value))
    if str:
        str = str.split(';')
        return [s.strip() for s in str]
    return None


def user_edit_short_text(sermon_code, title, value, choices = None, pattern = None):
    """Let user edit a value"""
    subtitle = '[dim]Lämna tomt för att behålla värdet.[/dim]'
    print()
    console.print(
        Panel(f"{value}",
        title=f"[key]Ändra {title}[/key]",
        title_align='left', 
        subtitle=subtitle,
        subtitle_align='right',
        box=box.ROUNDED 
        )
    )
    
    new_value = user_input('Nytt värde', default=None, choices=choices, pattern=pattern, allow_empty=True, blank_line=True)

    return new_value


def user_edit_generic_complex(sermon_code, title, data, fields, path = None):
    """Let user edit services, manuscripts, recordings and resources - all in one generic function."""

    clear_screen()

    # Build a table to show the data
    table = Table(title=None, box=box.SIMPLE, expand=False) # A table inside the panel
    table.add_column('  ', style='key', no_wrap=True)  # Index column
    for field in fields:  # Add column headers from the used fields
        table.add_column(field[1], style='title', no_wrap=False)

    for i in range(len(data)):  # Fill table with data
        item = data[i]
        index = 'ABCDEF'[i]  # Index for each row
        row = [index]
        for field in fields:
            value = str(getattr(item, field[0]))
            if value == 'None':
                value = ''
            if field[0] == 'file_name' and path:  # Add a link if a file
                value = get_file_link(path, value)

            row.append(value)  # Get the correct values
        table.add_row(*row)  # Add all rows

    print()
    console.print(  # Show table in panel
        Panel(table,
        title=f"[key]{sermon_code}: {title}[/key]",
        title_align='left', 
        box=box.ROUNDED 
        )
    )

    # Abort if no data to edit
    if not data:
        console.print(f"Det finns ingen {title} kopplad till denna predikan att redigera. Lägg till gudstjänst/manus/inspelning/resurs med [code]sermon add ...[/code]")
        Confirm.ask('Tryck enter för att fortsätta', default = True)
        return None

    txt = ''
    index = 1
    for field in fields:
        txt += f"[key]{index}.[/key] {field[1]}  "
        index += 1

    subtitle = '[dim]Lämna tomt för att behålla värdet.[/dim]'
    print()
    console.print(
        Panel(txt,
        title=f"[key]Ändra {title}[/key]",
        title_align='left', 
        subtitle=subtitle,
        subtitle_align='right',
        box=box.ROUNDED 
        )
    )

    new_value = user_input('Nytt värde', default=None, allow_empty=True, blank_line=True)
    return new_value


def user_edit_services(sermon_code, title, value):
    """Let user edit services in interactive mode"""
    #date, place, notes
    fields = [('date', 'Datum'), ('place', 'Plats'), ('notes', 'Kommentar')]
    return user_edit_generic_complex(sermon_code, title, value, fields)


def user_edit_manuscripts(sermon_code, title, value):
    """Let user edit manuscripts in interactive mode"""
    #file_name, version, date, notes
    fields = [('file_name', 'Filnamn'), ('version', 'Version'), ('date', 'Datum'), ('notes', 'Kommentar')]
    path = PATH_MANUSCRIPTS
    return user_edit_generic_complex(sermon_code, title, value, fields, path)


def user_edit_recordings(sermon_code, title, value):
    """Let user edit recordings in interactive mode"""
    #type, date, file_name, external_url, notes
    fields = [('type', 'Typ'), ('date', 'Datum'), ('file_name', 'Filnamn'), ('external_url', 'Extern url'), ('notes', 'Kommentar')]
    path = PATH_RECORDINGS
    return user_edit_generic_complex(sermon_code, title, value, fields, path)


def user_edit_resources(sermon_code, title, value):
    """Let user edit resources in interactive mode"""
    #file_name, title, notes
    fields = [('file_name', 'Filnamn'), ('title', 'Rubrik'), ('notes', 'Kommentar')]
    path = PATH_RESOURCES
    return user_edit_generic_complex(sermon_code, title, value, fields, path)



