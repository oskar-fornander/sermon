#app/cli.py

import sys
import traceback
from app.errors import SermonError
from app.config import CONFIG, DB_FILE
from app.config import init_environment
from app.presentation.common import render_info_panel
import typer
from typer.core import TyperGroup

COMMAND_ORDER = [
    'list', 'search', 'show',               # Group 0
    'new', 'edit', 'open',                  # Group 1
    'export', 'files', 'backup', 'delete'   # Group 2
]

class OrderedGroup(TyperGroup):
    def list_commands(self, ctx):
        # Return commands in the specified order in order to show them like this in the help text
        all_commands = list(self.commands.keys())
        #Sort by COMMAND_ORDER. Commands not i list are placed last
        return sorted(all_commands, key=lambda x: COMMAND_ORDER.index(x) if x in COMMAND_ORDER else 999)


init_environment()

from app.commands import list as list_commands
from app.commands import export as export_commands
from app.commands import open as open_commands
from app.commands.edit import edit
from app.commands import files as files_commands

from app.commands.show import show
from app.commands.search import search
from app.commands.new import new
from app.commands.delete import delete
from app.commands.backup import backup

app = typer.Typer(
        cls=OrderedGroup, 
        help = 'Predikoarkiv',
        no_args_is_help=True,
        add_completion=False
)

# Register commands. The order they should be shown in --help are defined above
command_groups = ('Överblick & sök', 'Innehållshantering', 'Export & underhåll')  # Headings for command groups - only for user friendly readability

# Single commands
app.command(rich_help_panel=command_groups[0])(search)
app.command(rich_help_panel=command_groups[0])(show)
app.command(rich_help_panel=command_groups[1])(new)
app.command(rich_help_panel=command_groups[1])(edit)
app.command(rich_help_panel=command_groups[2])(delete)
app.command(rich_help_panel=command_groups[2])(backup)

# Sub commands 
app.add_typer(list_commands.app, name = 'list', rich_help_panel=command_groups[0])
app.add_typer(open_commands.app, name = 'open', rich_help_panel=command_groups[1])
app.add_typer(export_commands.app, name = 'export', rich_help_panel=command_groups[2])
app.add_typer(files_commands.app, name = 'files', rich_help_panel=command_groups[2])



def run():
    try:
        app()
    except SermonError as e:
        render_info_panel(title='[error]Fel[/error]', content=f"{e}")
        sys.exit(1)
    except Exception as e:
        msg = f"Ett oväntat fel inträffade: {e}\n"
        render_info_panel(title='[error]Fel[/error]', content=msg)
        traceback.print_exc()  # file and row number
        sys.exit(1)



if __name__ == '__main__':
    run()

