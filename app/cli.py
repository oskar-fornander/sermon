
from app.config import CONFIG, DB_FILE
from app.config import init_environment
import typer

init_environment()

from app.commands import list as list_commands
from app.commands import export as export_commands
from app.commands import open as open_commands
from app.commands.edit import edit

from app.commands.show import show
from app.commands.search import search
from app.commands.new import new
from app.commands.delete import delete
from app.commands.backup import backup

app = typer.Typer(help = 'Predikoarkiv')

#Sub commands
app.add_typer(list_commands.app, name = 'list')
app.add_typer(open_commands.app, name = 'open')
app.add_typer(export_commands.app, name = 'export')

#Single commands
app.command()(show)
app.command()(search)
app.command()(new)
app.command()(edit)
app.command()(delete)
app.command()(backup)








if __name__ == '__main__':
    app()

