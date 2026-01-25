
from app.presentation.common import *




def user_edit(title, value):
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
    
    new_value = user_input('Nytt värde', default=None, choices=None, pattern=None, allow_empty=True, blank_line=True)

    if new_value:
        console.print(f"{title} uppdaterad till {new_value}")
    else:
        console.print(f"{title} lämnad oredigerad")

    return new_value



def render_edit_menu(title, options):
    """Show a menu for interactive editing"""

    menu = ''
    for i in range(len(options)):
        menu += f"[key]{i + 1}.[/key] {options[i]}  "

    subtitle = f"[bold][key]s[/key]: spara ändringar, [key]q[/key]: avbryt redigering[/bold]"
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



