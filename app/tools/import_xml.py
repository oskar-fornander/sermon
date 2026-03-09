#Import sermons from old xml-file into the new database by creating a new sqlite database file.
#This script is written by chatGPT
#Run this script like this: python3 -m app.tools.import_xml ../old_archive/sermons.xml
import sys
import html
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import traceback

from app.utils import PATTERN
from app.presentation.common import clear_screen, console
from app.config import init_environment, create_schema
import app.config as config
from app.services.sermon_draft import SermonDraft, ServiceDraft, ManuscriptDraft, RecordingDraft, ResourceDraft, validate_sermon_draft
from app.db import create_sermon_in_database, get_sermon_id, update_related_sermons
from app.services.edit_sermon import interactive_edit_sermon
from app.errors import ValidationError


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def decode(text):
    if text is None:
        return None
    return html.unescape(text.strip())


def ask_yes_no(question):
    while True:
        answer = input(f"{question} [y/n]: ").lower().strip()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False


# ---------------------------------------------------------
# Parse XML → SermonDraft
# ---------------------------------------------------------

def parse_sermon(elem):

    code = elem.attrib.get("index")
    title = decode(elem.attrib.get("title"))
    context = decode(elem.attrib.get("context"))

    draft = SermonDraft(
        id=None,
        code=code,
        title=title,
        context=context,
    )

    dates = []
    for child in elem:

        tag = child.tag

        if tag == "reference":
            ref = decode(child.text)
            if ref:
                draft.bible_references.append(ref)

        elif tag == "introduction":
            draft.introduction = decode(child.text)

        elif tag == "message":
            draft.message = decode(child.text)

        elif tag == "comment":
            draft.notes = decode(child.text)

        elif tag == "report":
            draft.report = decode(child.text)

        elif tag == "related":
            related = decode(child.text)
            if related:
                draft.related_sermons.append(related)

        elif tag == "service":
            date = child.attrib.get("date")
            dates.append(date)
            place = decode(child.attrib.get("place"))
            if date and place:
                draft.services.append(
                    ServiceDraft(
                        id=None,
                        date=date,
                        place=place,
                        notes=decode(child.attrib.get("notice")),
                    )
                )

        elif tag == "manuscript":

            file_name = decode(child.text)
            date = dates.pop(0)

            if file_name:
                draft.manuscripts.append(
                    ManuscriptDraft(
                        id=None,
                        date=date,
                        file_name=file_name
                    )
                )

        elif tag == "resource":

            title = decode(child.attrib.get("title"))
            file_name = decode(child.text)

            if title:
                draft.resources.append(
                    ResourceDraft(
                        id=None,
                        title=title,
                        file_name=file_name
                    )
                )

        elif tag == "recording":
            
            type = child.attrib.get("type")
            file_name = decode(child.text)
            date = child.attrib.get("date")
            if file_name and date:
                external_url = None
                if 'http' in file_name:
                    external_url = file_name
                    file_name = None
                
                draft.recordings.append(
                    RecordingDraft(
                        id=None,
                        type=type,
                        date=date,
                        file_name=file_name,
                        external_url=external_url
                    )
                )

    return draft


# ---------------------------------------------------------
# Preview
# ---------------------------------------------------------

def preview_edit_confirm_draft(draft):

    edited_draft = interactive_edit_sermon(draft)
    if not edited_draft:  # Edit mode exited without saving
        if ask_yes_no(f"Inkludera predikan {draft.code} i importen?"):
            return draft
        else:
            return None
    return edited_draft



# ---------------------------------------------------------
# Parse XML file
# ---------------------------------------------------------

def load_xml(path):

    tree = ET.parse(path)
    root = tree.getroot()

    drafts = []

    for sermon in root.findall("sermon"):
        drafts.append(parse_sermon(sermon))

    return drafts


# ---------------------------------------------------------
# Create new database
# ---------------------------------------------------------

def create_database(path):

    if path.exists():
        raise RuntimeError(f"Database already exists: {path}")

    conn = get_connection(path)
    create_schema(conn)
    return conn

def get_connection(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row #Access via column names instead of indices
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

# ---------------------------------------------------------
# Import drafts
# ---------------------------------------------------------

def import_draft(conn, draft):

    try:
        validate_sermon_draft(draft)
    except ValidationError as e:
        console.print(f"Predikan {draft.code} importeras inte pga fel: \n  {e}")
        return
    try:
        create_sermon_in_database(draft, conn, include_related_sermons = False)  # Create sermons but do note save related sermons until all sermons are added
    except Exception as e:
        console.print(f"Fel vid skapande av predikan {draft.code}. Sparas inte i databasen. \n  {e}")

def import_related_sermons(conn, draft):

    try:
        sermon_id = get_sermon_id(draft.code, conn)
        update_related_sermons(conn, sermon_id, draft.related_sermons)  # Add related sermons
    except Exception as e:
        console.print(f"Fel när relaterade predikningar skulle läggas till för {draft.code}: \n  {e}")



def validate_drafts(drafts):

    no_errors = True
    for draft in drafts:
        try:
            validate_sermon_draft(draft)  # This validation function throws errors if something is wrong in the draft
        except ValidationError as e:
            console.print(f"> Validation Error i predikan [key]{draft.code}[/key]")
            console.print(f"    {e}")
            no_errors = False

    return no_errors


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    init_environment()
    clear_screen()

    if len(sys.argv) < 2:
        print("Usage: python -m app.tools.import_xml <xmlfile>")
        sys.exit(1)

    xml_path = Path(sys.argv[1])

    if not xml_path.exists():
        print("File not found:", xml_path)
        sys.exit(1)

    print("Loading XML...")
    drafts = load_xml(xml_path)

    print(f"\nFann {len(drafts)} predikningar för import\n")


    ask_yes_no("Letar efter fel i de predikningar som ska importeras. Fortsätta?")
    if not validate_drafts(drafts):
        if not ask_yes_no("Åtgärda felen före eller i importens förhandsgranskning, annars kommer inte predikningar med fel att importeras. Fortsätta?"):
            return
    else:
        console.print('Inga fel hittade.')

    edited_drafts = []  # Let user preview and edit sermons in interactive edit mode before import
    while True:
        q = input("Ange index för en predikan att granska/redigera/exkludera före import (t.ex. P001) eller 'q' för att gå vidare. ")
        if q == 'q':
            break
        if not PATTERN['code'].match(q):
            console.print('Felaktig kod.')
            continue
        draft = None
        for i in range(len(drafts)):
            if drafts[i].code == q:
                draft = drafts.pop(i)
                break
        if not draft:
            console.print('Predikan med denna kod finns inte i importen.')
            continue
        edited_draft = preview_edit_confirm_draft(draft)
        clear_screen()
        if not edited_draft:
            print(f"Hoppar över predikan {draft.code} vid import")
            continue
        edited_drafts.append(edited_draft)
    drafts.extend(edited_drafts)
    drafts.sort(key=lambda x: x.code)


    clear_screen()
    #if not ask_yes_no(f"Genomföra full import av {len(drafts)} predikningar efter förhandsgranskning och redigering?"):
        #return


    timestamp = datetime.now().isoformat()
    db_path = config.PATH_DATABASE / f"sermons_imported_{timestamp[:timestamp.find('.')]}.db"
    print("\nSkapar databas ...")
    conn = create_database(db_path)

    print("Importerar predikningar ...")
    for draft in drafts:
        with conn:
            import_draft(conn, draft)  # Add sermons to database (without related sermons)
    conn.close()
    conn = get_connection(db_path)
    for draft in drafts:
        with conn:
            import_related_sermons(conn, draft)  # Add related sermons to database
    conn.close()


    print(f"\nImport klar. {len(drafts)} predikningar importerade.")
    print("Databas:", db_path)
    print("Ersätt ev. befintlig databasfil med denna nyskapade fil och namnge den sermon.db")


if __name__ == "__main__":
    main()
