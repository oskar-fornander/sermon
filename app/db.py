# app/db.py

import sqlite3
from app.errors import DatabaseError, NotFoundError
from typing import List
from pathlib import Path
import yaml
from app.presentation.common import console
#from app.config import DB_FILE
import app.config as config

# --------------------
# Configuration and Connection
# --------------------

# functions ensure_database() and create_schema() are in app/config.py


def get_connection():
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row #Access via column names instead of indices
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


# --------------------
# Basic functions (sermon)
# --------------------

def get_sermon_by_code(code: str, conn = None):
    """Get a sermon by its code (e.g. 'P371')"""
    new_conn = False
    if conn is None:
        new_conn = True
        conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM sermon WHERE code = ?",
            (code,)
        )
        row = cur.fetchone()
        if row is None:
            raise NotFoundError(f"Predikan [key]{code}[/key] finns inte. (Ange predikokoden i formatet P001.)")
        if new_conn:
            conn.close()
        return row
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")
    finally:
        if new_conn:
            conn.close()


def get_sermon_by_id(id: int, conn = None):
    """Get a sermon by its internal database id"""
    new_conn = False
    if conn is None:
        new_conn = True
        conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM sermon WHERE id = ?",
            (id,)
        )
        row = cur.fetchone()
        if row is None:
            raise NotFoundError(f"Predikan finns inte.")
        if new_conn:
            conn.close()
        return row
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")
    finally:
        if new_conn:
            conn.close()


def get_sermon_id(code: str, conn = None) -> int:
    """Get the sermon id (internal for database) based on its code (e.g. 'P371')"""
    row = get_sermon_by_code(code, conn)
    return row['id']


def get_sermon_code(id: int, conn = None) -> str:
    """Get the sermon code (P001) based on its internal database id"""
    row = get_sermon_by_id(id, conn)
    return row['code']


def sermon_exists(code: str, conn = None) -> True|False:
    """Test if a certain sermon code exist in database or not"""
    # This function might not be used, instead used database functions throw errors
    #if not get_sermon_by_code(code):
        #return False
    #return True
    new_conn = False
    if conn is None:
        new_conn = True
        conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM sermon WHERE code = ?",
            (code,)
        )
        row = cur.fetchone()
        if new_conn:
            conn.close()

        if row is None:
            return False
        return True
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")


def query_sermons(sort: str = 'code', limit: int = 0, query: [str] = [], bible_only: bool = False, date: str = None, date_from: str = None, date_to: str = None, year: int = None, month: int = None, place: str = None, report: str = None, must_have_recording: bool = False):
    """Make a query for sermons"""

    if sort == 'date':  # When listed by date the service date must be included form the service table
        sql = """
        SELECT sermon.code, service.date
        FROM service
        JOIN sermon ON service.sermon_id = sermon.id
        """
    else:  # sort == 'code'
        sql = """
        SELECT sermon.code
        FROM sermon
        """

    conditions = []
    params = []

    if query:  # Search query
        for term in query:  # Search for each term if more than one
            if bible_only:  # Search only in bible references
                conditions.append("""
            EXISTS (
                SELECT 1 FROM bible_reference
                WHERE bible_reference.sermon_id = sermon.id
                AND LOWER(bible_reference.reference_text) LIKE ?
            ) """)
                params.append(f"%{term.lower()}%")
                continue
            # Otherwise, search in all fields:
            conditions.append("""
            (
                LOWER(sermon.title) LIKE ?
                OR LOWER(sermon.context) LIKE ?
                OR LOWER(sermon.introduction) LIKE ?
                OR LOWER(sermon.message) LIKE ?
                OR LOWER(sermon.notes) LIKE ?
                OR EXISTS (
                    SELECT 1 FROM manuscript
                    WHERE manuscript.sermon_id = sermon.id
                    AND LOWER(manuscript.notes) LIKE ?
                )
                OR EXISTS (
                    SELECT 1 FROM service
                    WHERE service.sermon_id = sermon.id
                    AND LOWER(service.notes) LIKE ?
                )
                OR EXISTS (
                    SELECT 1 FROM recording
                    WHERE recording.sermon_id = sermon.id
                    AND LOWER(recording.notes) LIKE ?
                )
                OR EXISTS (
                    SELECT 1 FROM resource
                    WHERE resource.sermon_id = sermon.id
                    AND LOWER(resource.notes) LIKE ?
                )
                OR EXISTS (
                    SELECT 1 FROM bible_reference
                    WHERE bible_reference.sermon_id = sermon.id
                    AND LOWER(bible_reference.reference_text) LIKE ?
                )
            )
            """)
            for _ in range(10):  # Make sure to add as many parameters (the same search term) as there are queries above
                params.append(f"%{term.lower()}%")  # Make search case insensitive also for åäö with .lower() and LOWER()

    sub_conditions = []  # These are used for EXISTS() when query for service
    sub_params = []

    # Filter by start and end date 
    if sort == 'date':
        if date_from:
            conditions.append("""
            service.date >= ?
            """)
            params.append(date_from)
        if date_to:
            conditions.append("""
            service.date <= ?
            """)
            params.append(date_to)
    else:  # code
        if date_from:
            sub_conditions.append("""
                service.date >= ?
                """)
            sub_params.append(date_from)
        if date_to:
            sub_conditions.append("""
                service.date <= ?
                """)
            sub_params.append(date_to)


    if date:  # Filter by ISO date: YYYY-MM-DD
        if sort == 'date':
            conditions.append("""
            service.date = ?
            """)
            params.append(date)
        else:  # code
            sub_conditions.append("""
                service.date = ?
                """)
            sub_params.append(date)
    elif year or month:  # Filter by year and/or month (if both are given we assume both will apply to the same date, therefore we have a common search)
        year = str(year) if year else '%'  # Use asterisk for year if no year is given, works with LIKE
        month = str(month) if month else '%'  # (Note: SQLite only supports %m (month with leading 0), %Y (year) and %d (day) in strftime().)
        if sort == 'date':
            conditions.append("""
            (
                strftime('%Y', service.date) LIKE ?
                AND CAST(strftime('%m', service.date) AS INTEGER) LIKE ?
            )
            """)
            params.append(year)
            params.append(month)
        else:  # code
            sub_conditions.append("strftime('%Y', service.date) LIKE ? ")
            sub_conditions.append("CAST(strftime('%m', service.date) AS INTEGER) LIKE ? ")
            sub_params.append(year)
            sub_params.append(month)

    if place:  # Filter by place
        if sort == 'date':
            conditions.append("""
            LOWER(service.place) LIKE ?
            """)
            params.append(f"%{place.lower()}%")
        else:
            sub_conditions.append("""
                LOWER(service.place) LIKE ?""")
            sub_params.append(f"%{place.lower()}%")

    if report:  # Filter by report
        conditions.append("""
            sermon.report == ?
            """)
        params.append(report)
    
    if must_have_recording:  # Filter out sermons that have at least one recording (file or url)
        conditions.append("""
            EXISTS (
                SELECT 1 FROM recording
                WHERE recording.sermon_id = sermon.id
            )
            """)


    if sub_conditions:
        conditions.append(f"""
            EXISTS (
                SELECT 1 FROM service
                WHERE service.sermon_id = sermon.id
                AND {'AND '.join(sub_conditions)}
            ) """)
        params.extend(sub_params)

    if conditions:
        sql += "WHERE " + "AND".join(conditions)  # Add all conditions ANDed

    if sort == 'date':
        sql += "\n        ORDER BY service.date DESC"  # Always search from the end of the database; i.e. include the last sermons in the search - based on date of service
    else:  # code
        sql += "\n        ORDER BY sermon.code DESC"  # Always search from the end of the database; i.e. include the last sermons in the search

    if limit:  # Limit the number of hits to show?
        sql += "\n        LIMIT ?"
        params.append(limit)

    #console.print(sql)  # DEBUG: show the search performed in database
    #console.print(params)

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, params)
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")

def query_services(query: str = None, year: int = None, month: int = None, place: str = None, report: str = None, must_have_recording: bool = False, limit: int = 0):
    """Make a query for services"""
    pass


def list_sermon_codes():
    """List sermon codes by code"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT 
                sermon.code 
            FROM sermon
            ORDER BY sermon.code
            """
        )
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")


def list_service_dates():
    """List sermons by service date"""
    conn = get_connection()
    cur = conn.cursor()
    try:
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
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")


def get_last_sermon_code():
    """Get the code of the last sermon in the database."""
    sermons = list_sermon_codes()
    if len(sermons) == 0:
        return 'P000'  # special case for first sermon if empty database
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
    try:
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
        if row is None:
            raise NotFoundError(f"Sermon for date {date} not found.")
        return row
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")

def get_last_place():
    """Get the place for the last service"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT place
            FROM service
            ORDER BY date
            """
        )
        row = cur.fetchone()
        conn.close()
        if row is None:
            raise NotFoundError(f"No service found")
        return row
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")

def get_services_for_sermon(code: str):
    """Get all services connected to this sermon"""
    conn = get_connection()
    cur = conn.cursor()
    try:
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
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")

def get_manuscripts_for_sermon(code: str):
    """Get all manuscripts connected to this sermon, ordered by version"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT manuscript.* FROM manuscript 
            JOIN sermon ON manuscript.sermon_id = sermon.id 
            WHERE sermon.code = ?
            ORDER BY manuscript.date, manuscript.file_name
            """,
            (code,)
        )
        row = cur.fetchall()
        conn.close()
        return row
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")

def get_recordings_for_sermon(code: str):
    """Get all recordings connected to this sermon"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT recording.* FROM recording 
            JOIN sermon ON recording.sermon_id = sermon.id 
            WHERE sermon.code = ?
            ORDER BY recording.date, recording.type
            """,
            (code,)
        )
        row = cur.fetchall()
        conn.close()
        return row
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")

def get_resources_for_sermon(code: str):
    """Get all resources connected to this sermon"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT resource.* FROM resource 
            JOIN sermon ON resource.sermon_id = sermon.id 
            WHERE sermon.code = ?
            ORDER BY resource.title, resource.file_name
            """,
            (code,)
        )
        row = cur.fetchall()
        conn.close()
        return row
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")


def get_bible_references_for_sermon(code: str):
    """Get all bible references connected to this sermon"""
    conn = get_connection()
    cur = conn.cursor()
    try:
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
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")

def get_related_sermons_for_sermon(code: str):
    """Get all related sermons connected to this sermon"""
    id = get_sermon_id(code)
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT s.code, s.title
            FROM sermon_relation r
            JOIN sermon s
            ON s.id = r.related_sermon_id
            WHERE r.sermon_id = ?

            UNION

            SELECT s.code, s.title
            FROM sermon_relation r
            JOIN sermon s
            ON s.id = r.sermon_id
            WHERE r.related_sermon_id = ?
            """,
            (id, id)
        )
        row = cur.fetchall()
        conn.close()
        return row
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")


def get_all_manuscripts():
    """Get all manuscripts in database"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT manuscript.file_name, sermon.code FROM manuscript 
            JOIN sermon ON manuscript.sermon_id = sermon.id 
            ORDER BY sermon.code
            """
        )
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")

def get_all_recordings():
    """Get all recordings in database"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT recording.file_name, sermon.code FROM recording 
            JOIN sermon ON recording.sermon_id = sermon.id 
            WHERE recording.file_name IS NOT NULL
            AND TRIM(recording.file_name) != ''
            ORDER BY sermon.code
            """
        )
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")

def get_all_resources():
    """Get all resources in database"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT resource.file_name, sermon.code FROM resource 
            JOIN sermon ON resource.sermon_id = sermon.id 
            ORDER BY sermon.code
            """
        )
        rows = cur.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        raise DatabaseError(f"Databasfel: {e}")





# --------------------
# Load from database with SermonDraft
# --------------------

# load_sermon_as_draft() is in services/sermon_draft.py

# --------------------
# Write to database from SermonDraft
# --------------------
def create_sermon_in_database(draft: "SermonDraft", conn = None, include_related_sermons = True):
    """Create a new sermon in the database based on data in the draft. Validation is already made in create_sermon_from_draft in services/sermon_draft.py"""
    # Data is inserted into sermon and all other relevant tables
    # No sermon id exists before insertion in database
    new_conn = False
    if conn is None:
        new_conn = True
        conn = get_connection()
    try:
        with conn:
            # 1. Insert sermon
            sermon_id = insert_sermon_row(conn, draft)  # Insert new row in sermon table
            draft.id = sermon_id  # Update sermon draft with the correct sermon id
            #console.print('sermon id: ', sermon_id)

            # 2. Insert other resources for this sermon (using update functions below)
            update_services(conn, sermon_id, draft.services, delete_missing=False)  # Insert new services using update function (ok since delete_missing is False and there is no service.id)
            update_manuscripts(conn, sermon_id, draft.manuscripts, delete_missing=False)
            update_recordings(conn, sermon_id, draft.recordings, delete_missing=False)
            update_resources(conn, sermon_id, draft.resources, delete_missing=False)
            update_bible_references(conn, sermon_id, draft.bible_references)
            if include_related_sermons:
                update_related_sermons(conn, sermon_id, draft.related_sermons)
        #conn.commit()  # conn.commit() and conn.rollback() are executed automatically when using with conn.
    except sqlite3.Error as e:
        #conn.rollback()
        raise DatabaseError(f"Databasfel: {e}")
    finally:
        if new_conn:  # Close connection only if created inside this function
            conn.close()


def insert_sermon_row(conn, draft):  # Update sermon table
    """Skriv ny rad till huvudtabellen sermon"""
    cur = conn.cursor()
    cur.execute(  # Insert all properties for this row in the sermon table
        """
        INSERT INTO sermon
        (code, title, context, introduction, message, report, notes)
        VALUES(?, ?, ?, ?, ?, ?, ?)
        """,
        (
            draft.code, 
            draft.title, 
            draft.context, 
            draft.introduction, 
            draft.message, 
            draft.report,
            draft.notes 
         )
    )
    #console.print('Rows affected:', cur.rowcount)
    return cur.lastrowid  # Return the new sermon id for this particular sermon



# --------------------
# Update database from SermonDraft
# --------------------
def update_sermon_from_draft(draft: "SermonDraft"):
    """Uppdatera en befintlig predikan i databasen baserat på data i draft."""
    # sermon is UPDATED in database
    # other tables (manuscripts, recordings, etc.) are DELETED and RECREATED in database

    # update_sermon_from_draft gör:
    # 1. UPDATE sermon
    # 2. För varje barn-typ:
            # UPDATE där id finns
            # INSERT där id saknas
            # DELETE där id inte längre finns
    # 3. commit

    sermon_id = draft.id  # internal database id for this sermon
    conn = get_connection()

    try:
        with conn:
            update_sermon_row(conn, draft)  # Update sermon table
            update_services(conn, sermon_id, draft.services, delete_missing=True)  # Update services: UPDATE if id exists, INSERT if id is missing, DELETE if id is removed
            update_manuscripts(conn, sermon_id, draft.manuscripts, delete_missing=True)
            update_recordings(conn, sermon_id, draft.recordings, delete_missing=True)
            update_resources(conn, sermon_id, draft.resources, delete_missing=True)
            update_bible_references(conn, sermon_id, draft.bible_references)
            update_related_sermons(conn, sermon_id, draft.related_sermons)
    except Exception as e: 
        raise DatabaseError(f"Databasfel: {e}")
    finally:
        conn.close()


def update_sermon_row(conn, draft):  # Update sermon table
    """Uppdatera egenskaper för sermon i själva huvudtabellen sermon"""
    cur = conn.cursor()
    cur.execute(  # Update all properties for this row in the sermon table
        """
        UPDATE sermon 
        SET 
        code = ?,
        title = ?,
        context = ?,
        introduction = ?,
        message = ?,
        report = ?,
        notes = ?
        WHERE id = ?
        """,
        (
            draft.code, 
            draft.title, 
            draft.context, 
            draft.introduction, 
            draft.message, 
            draft.report,
            draft.notes, 
            draft.id
         )
    )
    #console.print('Updating sermon id:', draft.id)
    #console.print('Rows affected:', cur.rowcount)


def update_services(conn, sermon_id, services: List["ServiceDraft"], delete_missing=False):
    """Uppdatera gudstjänster för angiven sermon_id utifrån angiven lista med "ServiceDraft". Radera poster databasen som saknas i argumentets lista om True, annars lägg bara till. Om satt till False kan denna funktion användas för att lägga till ny post, skickad som lista."""
    cur = conn.cursor()
    if delete_missing:  # 3. Delete post in database that is not represented in the given list of drafts - only if delete_missing is set to True.
        db_services = get_services_for_sermon(get_sermon_code(sermon_id))  # Current services in database
        ids = [s.id for s in services]  # All id:s in given argument
        for db_service in db_services:  # Check all
            if db_service['id'] not in ids:
                # Remove this one
                cur.execute(
                    """
                    DELETE FROM service
                    WHERE id = ?
                    """,
                    (db_service['id'],)
                )

    for service in services:
        if service.id:  # 1. UPDATE if id exists (it means the post is not new but might be changed)
            cur.execute(
                """
                UPDATE service
                SET
                date = ?,
                place = ?,
                notes = ?
                WHERE id = ?
                """,
                (
                    service.date, 
                    service.place, 
                    service.notes, 
                    service.id
                )
            )
        else:  # 2. INSERT if id does not exist (it means this is a newly created one)
            cur.execute(
                """
                INSERT INTO service
                (sermon_id, date, place, notes)
                VALUES(?, ?, ?, ?)
                """,
                (
                    sermon_id, 
                    service.date,
                    service.place,
                    service.notes
                )
            )


def update_manuscripts(conn, sermon_id, manuscripts: List["ManuscriptDraft"], delete_missing=False):
    """Uppdatera manuskript för angiven sermon_id utifrån angiven lista med "ManuscriptDraft". Radera poster databasen som saknas i argumentets lista om True, annars lägg bara till. Om satt till False kan denna funktion användas för att lägga till ny post, skickad som lista."""
    cur = conn.cursor()
    if delete_missing:  # 3. Delete post in database that is not represented in the given list of drafts - only if delete_missing is set to True.
        db_manuscripts = get_manuscripts_for_sermon(get_sermon_code(sermon_id))  # Current manuscripts in database
        ids = [s.id for s in manuscripts]  # All id:s in given argument
        for db_manuscript in db_manuscripts:  # Check all
            if db_manuscript['id'] not in ids:
                # Remove this one
                cur.execute(
                    """
                    DELETE FROM manuscript
                    WHERE id = ?
                    """,
                    (db_manuscript['id'],)
                )

    for manuscript in manuscripts:
        if manuscript.id:  # 1. UPDATE if id exists (it means the post is not new but might be changed)
            cur.execute(
                """
                UPDATE manuscript
                SET
                file_name = ?,
                date = ?,
                notes = ?
                WHERE id = ?
                """,
                (
                    manuscript.file_name,
                    manuscript.date, 
                    manuscript.notes, 
                    manuscript.id
                )
            )
        else:  # 2. INSERT if id does not exist (it means this is a newly created one)
            cur.execute(
                """
                INSERT INTO manuscript
                (sermon_id, file_name, date, notes)
                VALUES(?, ?, ?, ?)
                """,
                (
                    sermon_id, 
                    manuscript.file_name,
                    manuscript.date,
                    manuscript.notes
                )
            )


def update_recordings(conn, sermon_id, recordings: List["RecordingDraft"], delete_missing=False):
    """Uppdatera inspelning för angiven sermon_id utifrån angiven lista med "RecordingDraft". Radera poster databasen som saknas i argumentets lista om True, annars lägg bara till. Om satt till False kan denna funktion användas för att lägga till ny post, skickad som lista."""
    cur = conn.cursor()
    if delete_missing:  # 3. Delete post in database that is not represented in the given list of drafts - only if delete_missing is set to True.
        db_recordings = get_recordings_for_sermon(get_sermon_code(sermon_id))  # Current recordings in database
        ids = [s.id for s in recordings]  # All id:s in given argument
        for db_recording in db_recordings:  # Check all
            if db_recording['id'] not in ids:
                # Remove this one
                cur.execute(
                    """
                    DELETE FROM recording
                    WHERE id = ?
                    """,
                    (db_recording['id'],)
                )

    for recording in recordings:
        if recording.id:  # 1. UPDATE if id exists (it means the post is not new but might be changed)
            cur.execute(
                """
                UPDATE recording
                SET
                type = ?,
                date = ?,
                file_name = ?,
                external_url = ?,
                notes = ?
                WHERE id = ?
                """,
                (
                    recording.type,
                    recording.date, 
                    recording.file_name,
                    recording.external_url,
                    recording.notes, 
                    recording.id
                )
            )
        else:  # 2. INSERT if id does not exist (it means this is a newly created one)
            cur.execute(
                """
                INSERT INTO recording
                (sermon_id, type, date, file_name, external_url, notes)
                VALUES(?, ?, ?, ?, ?, ?)
                """,
                (
                    sermon_id, 
                    recording.type,
                    recording.date,
                    recording.file_name,
                    recording.external_url,
                    recording.notes
                )
            )


def update_resources(conn, sermon_id, resources: List["ResourceDraft"], delete_missing=False):
    """Uppdatera resurs för angiven sermon_id utifrån angiven lista med "ResourceDraft". Radera poster databasen som saknas i argumentets lista om True, annars lägg bara till. Om satt till False kan denna funktion användas för att lägga till ny post, skickad som lista."""
    cur = conn.cursor()
    if delete_missing:  # 3. Delete post in database that is not represented in the given list of drafts - only if delete_missing is set to True.
        db_resources = get_resources_for_sermon(get_sermon_code(sermon_id))  # Current resources in database
        ids = [s.id for s in resources]  # All id:s in given argument
        for db_resource in db_resources:  # Check all
            if db_resource['id'] not in ids:
                # Remove this one
                cur.execute(
                    """
                    DELETE FROM resource
                    WHERE id = ?
                    """,
                    (db_resource['id'],)
                )

    for resource in resources:
        if resource.id:  # 1. UPDATE if id exists (it means the post is not new but might be changed)
            cur.execute(
                """
                UPDATE resource
                SET
                file_name = ?,
                title = ?,
                notes = ?
                WHERE id = ?
                """,
                (
                    resource.file_name,
                    resource.title, 
                    resource.notes, 
                    resource.id
                )
            )
        else:  # 2. INSERT if id does not exist (it means this is a newly created one)
            cur.execute(
                """
                INSERT INTO resource
                (sermon_id, file_name, title, notes)
                VALUES(?, ?, ?, ?)
                """,
                (
                    sermon_id, 
                    resource.file_name,
                    resource.title,
                    resource.notes
                )
            )


def update_bible_references(conn, sermon_id, bible_references: List[str]):
    """Uppdatera bibelreferenser för angiven sermon_id utifrån angiven lista. Alla raderas och ersätts på nytt."""
    cur = conn.cursor()
    # Delete all posts in database with sermon_id
    cur.execute(
        """
        DELETE FROM bible_reference
        WHERE sermon_id = ?
        """,
        (sermon_id,)
    )
    # Add all bible references as new posts
    for bible_reference in bible_references:
        cur.execute(
            """
            INSERT INTO bible_reference
            (sermon_id, reference_text)
            VALUES(?, ?)
            """,
            (
                sermon_id, 
                bible_reference
            )
        )


def update_related_sermons(conn, sermon_id, related_sermon_codes: List[str]):
    """Uppdatera relaterade predikningar för angiven sermon_id utifrån angiven lista. Alla raderas och ersätts på nytt."""
    cur = conn.cursor()
    # Delete all posts in database with sermon_id
    cur.execute(
        """
        DELETE FROM sermon_relation
        WHERE sermon_id = ? OR related_sermon_id = ?
        """,
        (sermon_id, sermon_id)
    )
    # Add all related sermons as new posts
    for related_sermon_code in related_sermon_codes:
        related_sermon_id = get_sermon_id(related_sermon_code, conn)
        id1, id2 = sorted([sermon_id, related_sermon_id])
        cur.execute(
            """
            INSERT INTO sermon_relation
            (sermon_id, related_sermon_id)
            VALUES(?, ?)
            """,
            (
                id1, 
                id2
            )
        )


# --------------------
# Delete from database
# --------------------
def delete_sermon_from_database(sermon_id: int):
    """Radera en predikan ur databasen, och alla tillhörande filer"""
    # Data is removed from the database with cascading
    conn = get_connection()
    cur = conn.cursor()
    try:
        with conn:
            cur.execute(
                """
                DELETE FROM sermon
                WHERE id = ?
                """,
                (sermon_id,)
            )
    except Exception as e: 
        raise DatabaseError(f"Databasfel: {e}")
    finally:
        conn.close()






# --------------------
# 
# --------------------

# --------------------
# 
# --------------------












