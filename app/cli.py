
from app.utils import CONFIG, BASE_DIR, DB_PATH, ARCHIVE_ROOT, load_config, define_paths
define_paths()
load_config()
import typer


from app.commands import list as list_commands
from app.commands import add as add_commands
from app.commands import remove as remove_commands
from app.commands import export as export_commands
from app.commands import open as open_commands
from app.commands import edit

from app.commands.show import show
from app.commands.search import search
from app.commands.new import new
#from app.commands.edit import edit




app = typer.Typer(help = 'Predikoarkiv')

#Sub commands
app.add_typer(list_commands.app, name = 'list')
app.add_typer(open_commands.app, name = 'open')
app.add_typer(add_commands.app, name = 'add')
app.add_typer(remove_commands.app, name = 'remove')
app.add_typer(export_commands.app, name = 'export')
app.add_typer(edit.app, name = 'edit')

#Single commands
app.command()(show)
app.command()(search)
app.command()(new)
#app.command()(edit)



# CLI commands:
# 
# sermon list
# sermon show
# sermon open manuscript|recording|resource
# sermon search
# sermon new
# sermon edit
# sermon add service|manuscript|recording|resource|bible-reference
# sermon remove service|manuscript|recording|resource|bible-reference
# sermon export html|podcast
# 









if __name__ == '__main__':
    app()

