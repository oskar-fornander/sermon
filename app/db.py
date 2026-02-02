# app/db.py

import sqlite3
from pathlib import Path
import yaml
from app.services.sermon_draft import new_sermon_draft, new_service_draft, new_manuscript_draft, new_recording_draft, new_resource_draft

from app.utils import DB_PATH

# --------------------
# Configuration
# --------------------


# --------------------
# Connection
# --------------------

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row #Access via column names instead of indices
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


# --------------------
# Basic functions (sermon)
# --------------------

def get_sermon_by_code(code: str):
    """Get a sermon by its code (e.g. 'P371')"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM sermon WHERE code = ?",
        (code,)
    )
    row = cur.fetchone()
    conn.close()
    return row


def get_sermon_id(code:str) -> int:
    """Get the sermon id (internal for database) based on its code (e.g. 'P371')"""
    row = get_sermon_by_code(code)
    if row is None:
        raise ValueError(f'Predikan med kod {code} finns inte')
    return row['id']


def list_sermon_codes():
    """List sermon codes by code"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT 
            sermon.code 
        FROM sermon
        ORDER BY sermon.code
        """
    )
    row = cur.fetchall()
    conn.close()
    return row

def list_service_dates():
    """List sermons by service date"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT 
            service.date 
        FROM service
        JOIN sermon ON sermon.id = service.sermon_id
        ORDER BY service.date
        """
    )
    row = cur.fetchall()
    conn.close()
    return row


#def list_sermons(order_by: str = 'code'):
#    """List sermons by code or date"""
#    conn = get_connection()
#    cur = conn.cursor()
#    if order_by == 'date':
#        cur.execute(
#            """
#            SELECT 
#                service.date, 
#                service.place, 
#                service.notes AS service_notes, 
#                sermon.code, 
#                sermon.title,
#                sermon.report
#            FROM service
#            JOIN sermon ON sermon.id = service.sermon_id
#            ORDER BY service.date
#            """
#        )
#    else: #'code'
#        cur.execute(
#            """
#            SELECT 
#                sermon.code, 
#                sermon.title,
#                sermon.report
#            FROM sermon
#            ORDER BY sermon.code
#            """
#        )
#    row = cur.fetchall()
#    conn.close()
#    return row

def get_last_sermon_code():
    """Get the code of the last sermon in the database."""
    sermons = list_sermon_codes()
    last_sermon = sermons[-1]
    return last_sermon['code']

def get_all_sermon_codes():
    """Get a list of all sermon codes used in the database."""
    sermons = list_sermon_codes()
    codes = [sermon['code'] for sermon in sermons]
    return codes

def get_sermon_code_by_service_date(date: str):
    """Get code for a sermon based on the given service date"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT sermon.code
        FROM service
        JOIN sermon ON service.sermon_id = sermon.id
        WHERE service.date = ?
        """,
        (date,)
    )
    row = cur.fetchone()
    conn.close()
    return row

def get_last_place():
    """Get the place for the last service"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT place
        FROM service
        ORDER BY date
        """
    )
    row = cur.fetchone()
    conn.close()
    return row


def get_services_for_sermon(code: str):
    """Get all services connected to this sermon"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT service.* FROM service
        JOIN sermon ON service.sermon_id = sermon.id
        WHERE sermon.code = ?
        ORDER BY service.date
        """,
        (code,)
    )
    row = cur.fetchall()
    conn.close()
    return row


def get_manuscripts_for_sermon(code: str):
    """Get all manuscripts connected to this sermon, ordered by version"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT manuscript.* FROM manuscript 
        JOIN sermon ON manuscript.sermon_id = sermon.id 
        WHERE sermon.code = ?
        ORDER BY manuscript.date
        """,
        (code,)
    )
    row = cur.fetchall()
    conn.close()
    return row

def get_recordings_for_sermon(code: str):
    """Get all recordings connected to this sermon"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT recording.* FROM recording 
        JOIN sermon ON recording.sermon_id = sermon.id 
        WHERE sermon.code = ?
        ORDER BY recording.date
        """,
        (code,)
    )
    row = cur.fetchall()
    conn.close()
    return row

def get_resources_for_sermon(code: str):
    """Get all resources connected to this sermon"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT resource.* FROM resource 
        JOIN sermon ON resource.sermon_id = sermon.id 
        WHERE sermon.code = ?
        ORDER BY resource.title
        """,
        (code,)
    )
    row = cur.fetchall()
    conn.close()
    return row


def get_bible_references_for_sermon(code: str):
    """Get all bible references connected to this sermon"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT bible_reference.* FROM bible_reference 
        JOIN sermon ON bible_reference.sermon_id = sermon.id 
        WHERE sermon.code = ?
        ORDER BY bible_reference.reference_text
        """,
        (code,)
    )
    row = cur.fetchall()
    conn.close()
    return row

def get_related_sermons_for_sermon(code: str):
    """Get all related sermons connected to this sermon"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s2.code, s2.title FROM sermon_relation r
        JOIN sermon s1 ON s1.id = r.sermon_id
        JOIN sermon s2 ON s2.id = r.related_sermon_id
        WHERE s1.code = ?
        """,
        (code,)
    )
    row = cur.fetchall()
    conn.close()
    return row


# --------------------
# Load and write to database with sermonDraft
# --------------------

def load_sermon_as_draft(sermon_code: str) -> sermonDraft:
    """Hämta data om en predikan och returnera som ett draft."""

    # Get data from the database
    sermon = get_sermon_by_code(sermon_code)
    services = get_services_for_sermon(sermon_code)
    manuscripts = get_manuscripts_for_sermon(sermon_code)
    recordings = get_recordings_for_sermon(sermon_code)
    resources = get_resources_for_sermon(sermon_code)
    bible_references = get_bible_references_for_sermon(sermon_code)
    related_sermons = get_related_sermons_for_sermon(sermon_code)

    # Convert that data into a sermonDraft
    sermon_draft = new_sermon_draft(sermon)  # Create a new sermonDraft with data from the given sermon
    sermon_draft.services = [new_service_draft(s) for s in services]  # The same for all sub tables (some may be more than one element in a list)
    sermon_draft.manuscripts = [new_manuscript_draft(m) for m in manuscripts]
    sermon_draft.recordings = [new_recording_draft(r) for r in recordings]
    sermon_draft.resources = [new_resource_draft(r) for r in resources]
    #sermon_draft.bible = '; '.join([b['reference_text'] for b in bible_references])  # text
    #sermon_draft.related = ', '.join([s['code'] for s in related_sermons])
    sermon_draft.bible = [b['reference_text'] for b in bible_references]  # list
    sermon_draft.related = [s['code'] for s in related_sermons]

    return sermon_draft


def create_sermon_from_draft(draft: sermonDraft):
    """Skapa en ny predikan i databasen baserat på data i draft."""
    pass

def update_sermon_from_draft(draft: sermonDraft):
    """Uppdatera en befintlig predikan i databasen baserat på data i draft."""
    pass



# --------------------
# 
# --------------------

# --------------------
# 
# --------------------












