
from app.presentation.common import *
import os
import shutil
import tempfile
import subprocess
import time
from app.config import PATH_MANUSCRIPTS, PATH_RECORDINGS, PATH_RESOURCES
from app.utils import get_file_link, PATTERN
from app.services.sermon_draft import deep_copy, new_service_draft, new_manuscript_draft, new_recording_draft, new_resource_draft


def render_edit_menu(title, options, show_menu_options=False):
    """Show a menu for interactive editing"""

    if show_menu_options:
        menu = ''
        for i in range(len(options)):
            menu += f"[key]{i + 1}.[/key]{NBSP}{options[i]}  "
    else:
        menu = f"Ange vilket fält du vill redigera. Enter (tomt) behåller värdet, '-' rensar (om tillåtet). I översikten markeras vilka fält som är ändrade. Spara med [key]s[/key] och avbryt med [key]q[/key]."

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
            new_value = f.read().strip()
            if new_value == value:  # No changes
                return None
            return new_value
    finally:
        os.unlink(path)



def user_edit_short_text_list(sermon_code, title, value, separator=';'):
    """Conver list to string before edit"""
    str = user_edit_short_text(sermon_code, title, f"{separator} ".join(value))
    if str:
        str = str.split(separator)
        return [s.strip() for s in str]
    return None


def user_edit_short_text(sermon_code, title, value, choices = None, pattern = None):
    """Let user edit a value"""
    subtitle = f"[dim]Enter (tomt) behåller värdet, '-' rensar (om tillåtet).[/dim]"
    if not value:
        value = '–'
    print()
    console.print(
        Panel(f"{value}",
        title=f"[key]Ändra {title.lower()}[/key]",
        title_align='left', 
        subtitle=subtitle,
        subtitle_align='right',
        box=box.ROUNDED 
        )
    )
    
    new_value = user_input(title, default=None, choices=choices, pattern=pattern, allow_empty=True, blank_line=True)

    return new_value


def user_edit_generic_complex(sermon_code, title, data, fields, path = None, new_instance = None, pending_file_deletions=None):
    """Let user edit services, manuscripts, recordings and resources - all in one generic function."""

    original_data = deep_copy(data)
    edited = []  # Save the edited posts as (row, field) to highlight them
    files_to_delete = []  # Save files for deletion


    def row_index(i):
        """Get a letter/number index for the row"""
        if isinstance(i, int) or i.isdigit():
            return 'ABCDEFGH'[i]  # return a letter: A, B, C, ...
        return 'ABCDEFGH'.index(i)  # return a digit: 1, 2, 3, ...

    def show_edit_screen(selected_row = None, selected_column = None):
        """Build a table to show the data"""
        clear_screen()
        table = Table(title=None, box=box.SIMPLE, expand=False) # A table inside the panel
        table.add_column('  ', style='key', justify='right', no_wrap=True)  # Index column
        index = 1
        for field in fields:  # Add column headers from the used fields along with index for selection
            table.add_column(f"[key]{index}.[/key] {field[1]}", style='', no_wrap=False)
            index += 1
        table.add_column(f"[key]x.[/key] Radera", style='', no_wrap=False)

        for i in range(len(data)):  # Fill table with data
            item = data[i]
            row = ['  ']
            if i == selected_row:
                row = ['▶ ']  # Mark the selected row
            index = row_index(i)  # Index for each row
            row[0] += index
            if item is None:  # Add empty place holder for delted row
                row.append('[deleted][RADERAD][/deleted]')
                row.extend([''] * (len(fields) - 1))
                table.add_row(*row)
                continue
            for field in fields:
                value = str(getattr(item, field[0]))
                if value == 'None':
                    value = ''
                if field[0] == 'file_name' and path:  # Add a link if a file
                    value = get_file_link(path, value)
                if (i, field[0]) in edited:  # Mark the edited values
                    value = f"[edited]{value}[/edited]"
                if i == selected_row and selected_column and field[1] == fields[selected_column - 1][1]:  # Mark cell as selected
                    value = f"[selected]{value}[/selected]"
                row.append(value)  # Get the correct values
            row.append('[key]x[/key]')  # Delete row
            if selected_row is not None and i != selected_row:
                row = [f"[not_selected]{x}[/not_selected]" for x in row]  # Mark all non selected rows as not selected
            table.add_row(*row)  # Add all rows
        #table.add_row('')

        text_add_row = ''
        if selected_row is None:
            text_add_row = f" [key]+[/key] Lägg till {title.lower()}"  # Show only if row is not selected
        content = Group(table, text_add_row)
        print()
        console.print(  # Show table in panel
            Panel(content,
            title=f"[key]{sermon_code}: {title}[/key]",
            title_align='left', 
            box=box.ROUNDED 
            )
        )

        # Show what to do
        subtitle = f"[bold][key]s[/key]: spara, [key]q[/key]: avbryt[/bold]"
        print()
        console.print(
            Panel(f"Välj vad du vill redigera. Enter (tomt) behåller värdet, '-' rensar (om tillåtet). Lägg till {title.lower()} med [key]+[/key] och radera vald rad med [key]x[/key].",
                title=f"[title]Redigera {title.lower()}[/title]",
                title_align='left', 
                subtitle=subtitle,
                subtitle_align='right',
                box=box.ROUNDED 
            )
        )
        print()

    def add_row():
        """Add new row"""
        new_row = new_instance(sermon_code=sermon_code)  # Create a new draft of the correct type
        data.append(new_row)  # Add this new empty item to the list
        for i in range(len(fields)):  # Mark whole row as edited
            edited.append((len(data) - 1, fields[i][0]))  # Used to indicate in preview what was just changed

    def delete_row():
        if Confirm.ask(f"Är du säker på att du vill radera {title.lower()} {row_index(row)}?", default = False):
            if hasattr(data[row], 'file_name'):  # If there is a file to remove
                file_name = data[row].file_name
                if file_name:
                    if Confirm.ask(f"Radera filen {file_name}?", default = True):
                        file = path / file_name
                        files_to_delete.append(file)  # Add file for deletion after edit
            #data.pop(row)  # Remove from data
            data[row] = None  # Remove data but keep a place holder - a better user experience

    def save():
        # Save all changes and return to main edit view
        # First, make sure all file names are unique: manuscript, recording and resource
        file_names = [getattr(data[r], 'file_name', None) for r in range(rows)]
        file_names = [f for f in file_names if f]  # Remove empty strings
        external_urls = [getattr(data[r], 'external_url', None) for r in range(rows)]
        external_urls = [f for f in external_urls if f]
        if len(file_names) != len(set(file_names)):
            user_confirmation(f"Kan inte spara: filnamn måste vara unika. Ändra och försök spara igen.")
            return None  # Do not save and exit
        if len(external_urls) != len(set(external_urls)):
            user_confirmation(f"Kan inte spara: externa url:er måste vara unika. Ändra och försök spara igen.")
            return None  # Do not save and exit

        # Save:
        for file in files_to_delete:  # Save files for pending deletion only when saving
            pending_file_deletions.add(file) 
        return [d for d in data if d is not None]  # Return all data but the None placeholders for deleted posts



    while True:  # Edit until escape edit mode
        rows = len(data)
        row = None
        item = None

        ## A. SELECT ROW
        # 1. no rows -> Add a row or quit are the only ptions if no row exists
        if rows == 0:
            show_edit_screen(selected_row = None)
            row = user_choice(title='Val', options=['s', 'q', '+'])

        # 2. one or more rows -> Select row of table if one or more, or quit or save
        elif rows >= 1:
            show_edit_screen(selected_row = None)
            row = user_choice(title='Rad', options='A B C D E F G H '[:2 * len(data)].strip().split(' ') + ['s', 'q', '+'])

        if row == 's':  # Save
            save_value = save()
            if save_value is not None:
                return save_value
            continue
        elif row == 'q':  # Quit without saving
            return None  
        elif row == '+':  # Add new row
            add_row()
            continue
        else:
            row = row_index(row)  # A row is selected
            if data[row] is None:  # An empty placeholder (deleted row) is selected
                continue

        ## B. SELECT ITEM/COLUMN
        show_edit_screen(selected_row=row)  # Show with selected row marked
        item = user_choice(title='Kolumn', options=[str(x + 1) for x in range(len(fields))] + ['x', 's', 'q'])

        if item == 's':
            save_value = save()
            if save_value is not None:
                return save_value
            continue
        elif item == 'q':
            return None  # Quit
        elif item == 'x':
            delete_row()
            continue
        else:
            item = int(item)  # selected column

        show_edit_screen(selected_row=row, selected_column=item)


        ## C. ENTER NEW VALUE FOR SELECTED FIELD
        field_name = fields[item - 1][1]
        pattern = None  # Special patterns for some fields
        choices = None  # Defined choices for some
        if field_name.lower() == 'datum':
            pattern = PATTERN['date']
        elif field_name.lower() == 'filnamn':
            pattern = PATTERN['file_name']
        elif field_name.lower() == 'extern url':
            pattern = PATTERN['url']
        elif field_name.lower() == 'typ':
            choices = ['audio', 'video']

        invalid_choices = []  # None of these values are valid
        if field_name.lower() in ('filnamn', 'extern url'):  # Avoid invalid filenames like duplicates for manuscripts, recordings and resources, and external urls for recordings
            invalid_choices = [getattr(data[r], fields[item - 1][0], '') for r in range(rows) if r != row]
            invalid_choices = [choice for choice in invalid_choices if choice is not None]

        console.print(f"[dim]{field_name}: {getattr(data[row], fields[item - 1][0]) or ''}[/dim]")
        new_value = user_input(f"{field_name}", pattern=pattern, choices=choices, default=None, allow_empty=True, invalid_choices=invalid_choices, blank_line=True)


        if new_value:  # No change if empty: keep value
            if new_value == '-':  # Clear field if allowed
                if field_name.lower() in ['rubrik', 'kommentar', 'extern url'] or (field_name.lower() == 'filnamn' and title.lower() == 'inspelning'):  # Only these fields can be empty: title, comment and external url, and file name but only if for recording
                    setattr(data[row], fields[item - 1][0], '')
                else:
                    console.print('Detta fält får inte vara tomt')
                    time.sleep(1)
            else:
                setattr(data[row], fields[item - 1][0], new_value)  # Update value
                edited.append((row, fields[item - 1][0]))  # Used to indicate in preview what was just changed



def user_edit_services(sermon_code, title, value):
    """Let user edit services in interactive mode"""
    #date, place, notes
    fields = [('date', 'Datum'), ('place', 'Plats'), ('notes', 'Kommentar')]
    return user_edit_generic_complex(sermon_code, title, value, fields, new_instance=new_service_draft)


def user_edit_manuscripts(sermon_code, title, value, pending_file_deletions):
    """Let user edit manuscripts in interactive mode"""
    #file_name, version, date, notes
    fields = [('file_name', 'Filnamn'), ('date', 'Datum'), ('notes', 'Kommentar')]
    path = PATH_MANUSCRIPTS
    return user_edit_generic_complex(sermon_code, title, value, fields, path=path, new_instance=new_manuscript_draft, pending_file_deletions=pending_file_deletions)


def user_edit_recordings(sermon_code, title, value, pending_file_deletions):
    """Let user edit recordings in interactive mode"""
    #type, date, file_name, external_url, notes
    fields = [('type', 'Typ'), ('date', 'Datum'), ('file_name', 'Filnamn'), ('external_url', 'Extern url'), ('notes', 'Kommentar')]
    path = PATH_RECORDINGS
    return user_edit_generic_complex(sermon_code, title, value, fields, path=path, new_instance=new_recording_draft, pending_file_deletions=pending_file_deletions)


def user_edit_resources(sermon_code, title, value, pending_file_deletions):
    """Let user edit resources in interactive mode"""
    #file_name, title, notes
    fields = [('file_name', 'Filnamn'), ('title', 'Rubrik'), ('notes', 'Kommentar')]
    path = PATH_RESOURCES
    return user_edit_generic_complex(sermon_code, title, value, fields, path=path, new_instance=new_resource_draft, pending_file_deletions=pending_file_deletions)



