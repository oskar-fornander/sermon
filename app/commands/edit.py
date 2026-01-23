import typer
from app.services.edit_sermon import interactive_edit_sermon, update_sermon_code, update_sermon_title, update_sermon_context, update_sermon_introduction, update_sermon_message, update_sermon_report, update_sermon_notes
from app.db import load_sermon_as_draft, create_sermon_from_draft, update_sermon_from_draft


# sermon edit P371              # interaktivt läge
# sermon edit P371 title "..."  # direktläge


app = typer.Typer(help='Redigera predikan')

@app.callback(invoke_without_command=True)  # Default (interaktiv edit): sermon edit P371
def edit(ctx: typer.Context, sermon_code: str):
    """Interaktiv redigering av en predikan"""
    ctx.obj = {'sermon_code': sermon_code}  # Make sermon_code available for all sub commands
    if ctx.invoked_subcommand is None:
        print(f"interactive edit: {sermon_code}")
        sermon_draft = load_sermon_as_draft(sermon_code)
        updated_sermon_draft = interactive_edit_sermon(sermon_draft)
        update_sermon_from_draft(updated_sermon_draft)

        

@app.command()
def code(ctx: typer.Context, code: str):
    """Ändra predikokod"""
    sermon_code = ctx.obj['sermon_code']
    update_sermon_code(sermon_code, code)

@app.command()
def title(ctx: typer.Context, title: str):  # sermon edit title P371 'Ny titel'
    """Ändra titel"""
    sermon_code = ctx.obj['sermon_code']
    print(f"ändra titel: {sermon_code}")
    update_sermon_title(sermon_code, title)

@app.command()
def context(ctx: typer.Context, context: str):
    """Ändra sammanhang"""
    sermon_code = ctx.obj['sermon_code']
    update_sermon_context(sermon_code, context)

@app.command()
def introduction(ctx: typer.Context, introduction: str):
    """Ändra introduktion"""
    sermon_code = ctx.obj['sermon_code']
    update_sermon_introduction(sermon_code, introduction)

@app.command()
def message(ctx: typer.Context, message: str):
    """Ändra budskap"""
    sermon_code = ctx.obj['sermon_code']
    update_sermon_message(sermon_code, message)

@app.command()
def report(ctx: typer.Context, report: str):
    """Ändra omdöme"""
    sermon_code = ctx.obj['sermon_code']
    update_sermon_report(sermon_code, report)

@app.command()
def notes(ctx: typer.Context, notes: str):
    """Ändra kommentar"""
    sermon_code = ctx.obj['sermon_code']
    update_sermon_notes(sermon_code, notes)



@app.command()
def service(ctx: typer.Context):
    """Redigera gudstjänster för predikan"""
    sermon_code = ctx.obj['sermon_code']
    edit_services_for_sermon(sermon_code)
    #Interactive editing for these objects

@app.command()
def manuscript(ctx: typer.Context):
    """Redigera manus"""
    sermon_code = ctx.obj['sermon_code']
    edit_manuscripts_for_sermon(sermon_code)

@app.command()
def recording(ctx: typer.Context):
    """Redigera inspelningar"""
    sermon_code = ctx.obj['sermon_code']
    edit_recordings_for_sermon(sermon_code)

@app.command()
def resource(ctx: typer.Context):
    """Redigera resurser"""
    sermon_code = ctx.obj['sermon_code']
    edit_resource_for_sermon(sermon_code)

@app.command()
def bible_reference(ctx: typer.Context):
    """Redigera bibelreferenser"""
    sermon_code = ctx.obj['sermon_code']
    edit_bible_references_for_sermon(sermon_code)

@app.command()
def related_sermon(ctx: typer.Context):
    """Redigera relaterade predikningar"""
    sermon_code = ctx.obj['sermon_code']
    edit_related_sermons_for_sermon(sermon_code)



