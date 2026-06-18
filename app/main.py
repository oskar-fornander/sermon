# app/main.py

import sys
import traceback
from app.errors import SermonError
from app.presentation.common import render_info_panel, clear_screen

def main():
    try:
        clear_screen()
        # 1. Initialize environment before importing cli.py
        # This prevents import-time errors when commands/services import constants.
        from app.config import init_environment
        init_environment()

        # 2. Import and run Typer CLI
        from app.cli import run
        run()

    except SermonError as e:
        render_info_panel(title='[error]Fel[/error]', content=f"{e}")
        sys.exit(1)
    except Exception as e:
        msg = f"Ett oväntat fel inträffade vid uppstart: {e}\n"
        render_info_panel(title='[error]Fel[/error]', content=msg)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
