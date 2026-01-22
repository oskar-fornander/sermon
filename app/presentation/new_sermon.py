
from app.presentation.common import *
from app.presentation.sermon_card import render_sermon_card



def render_info_panel(title: str, content: str='', subtitle: str=''):
    """Renders a small panel with title and maybe content."""
    print()
    console.print(
        Panel(content,
            title=f"[title]{title}[/title]",
            title_align='left', 
            subtitle=subtitle,
            subtitle_align='right',
            box=box.ROUNDED 
        )
    )
    print()



def user_input(title, default=None, choices=None, pattern=None, allow_empty=True):
    """Custom function to get user input from terminal via rich.prompt() with some safety functions"""
    while True:
        answer = Prompt.ask(title, choices=choices, default=default)
        if not answer:
            if allow_empty:
                answer = None  # or ''
                break
            else:
                console.print(f"[bold red]Värdet av [white dim]{title}[/white dim] får inte vara tomt.[/bold red]")
        elif pattern:
            if pattern.match(answer):
                break
            else:
                console.print(f"[bold red]Värdet av [white dim]{title}[/white dim] matchar inte formatet.[/bold red]")
        else:
            break
    print(f"--{answer}--")
    return answer





def show_sermon_draft(draft):
    """Show a sermon card for a draft, using an object instead of data from the databaes."""

    render_sermon_card(
            sermon=draft['sermon'], 
            services=draft['services'], 
            manuscripts=draft['manuscripts'], 
            recordings=draft['recordings'], 
            resources=draft['resources'], 
            bible_references=draft['bible_references'], 
            related_sermons=draft['related_sermons'])


