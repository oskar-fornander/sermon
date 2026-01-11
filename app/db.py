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
    conn.row_factory = sqlite3.Row #Access via column names
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




# --------------------
# 
# --------------------

# --------------------
# 
# --------------------

# --------------------
# 
# --------------------












