# app/db.py

import sqlite3
from pathlib import Path
import yaml

# --------------------
# Configuration
# --------------------


def load_config():
    config_path = Path(__file__).resolve().parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

CONFIG = load_config()
DB_PATH = Path(CONFIG['database']['path'] + CONFIG['database']['filename'])

# --------------------
# Connection
# --------------------

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row #Access via column names instead of indices
    conn.execute("PRAGMA foreign_keys = ON")
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


def list_sermons():
    """List sermons"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT code, title FROM sermon ORDER BY code ASC"
    )
    row = cur.fetchall()
    conn.close()
    return row


def get_services_for_sermon(code: str):
    """Get all services connected to this sermon"""
    #id = get_sermon_id(code) #use the internal id number
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        #"SELECT * FROM service WHERE sermon_id = ?",
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
        ORDER BY manuscript.version
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
# 
# --------------------

# --------------------
# 
# --------------------

# --------------------
# 
# --------------------












