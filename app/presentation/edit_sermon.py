
from app.presentation.common import *
import os
import shutil
import tempfile
import subprocess
import time



def find_fallback_editor() -> list[str] | None:
    for editor in ("nvim", "vim", "nano"):
        if shutil.which(editor):
            return [editor]
    return None

def user_edit_long_text(title, value):
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
    time.sleep(2)

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



def user_edit_short_text_list(title, value):
    """Conver list to string before edit"""
    str = user_edit_short_text(title, '; '.join(value))
    if str:
        str = str.split(';')
        return [s.strip() for s in str]
    return None


def user_edit_short_text(title, value, pattern = None):
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
    
    new_value = user_input('Nytt värde', default=None, choices=None, pattern=pattern, allow_empty=True, blank_line=True)

    if new_value:
        console.print(f"{title} uppdaterad till {new_value}")
    else:
        console.print(f"{title} lämnad oredigerad")

    return new_value



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



