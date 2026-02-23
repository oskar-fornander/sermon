-- schema.sql for sermon.db

CREATE TABLE IF NOT EXISTS sermon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    context TEXT,
    introduction TEXT,
    message TEXT,
    report TEXT CHECK (report IN ('A','B','C') OR report IS NULL),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS service (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    place TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (sermon_id) 
        REFERENCES sermon(id) 
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS manuscript (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    date TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (sermon_id) 
        REFERENCES sermon(id) 
        ON DELETE CASCADE
    UNIQUE (sermon_id, file_name)
);

CREATE TABLE IF NOT EXISTS recording (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    date TEXT NOT NULL,
    file_name TEXT,
    external_url TEXT,
    notes TEXT,
    FOREIGN KEY (sermon_id) 
        REFERENCES sermon(id) 
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS resource (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    title TEXT,
    notes TEXT,
    FOREIGN KEY (sermon_id) 
        REFERENCES sermon(id) 
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS bible_reference (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id INTEGER NOT NULL,
    reference_text TEXT NOT NULL,
    FOREIGN KEY (sermon_id) 
        REFERENCES sermon(id) 
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sermon_relation (
    sermon_id INTEGER NOT NULL,
    related_sermon_id INTEGER NOT NULL,
    PRIMARY KEY (sermon_id, related_sermon_id),
    FOREIGN KEY (sermon_id) 
        REFERENCES sermon(id) 
        ON DELETE CASCADE
    FOREIGN KEY (related_sermon_id) REFERENCES sermon(id)
);

CREATE INDEX idx_service_sermon ON service(sermon_id);
CREATE INDEX idx_manuscript_sermon ON manuscript(sermon_id);
CREATE INDEX idx_recording_sermon ON recording(sermon_id);
CREATE INDEX idx_resource_sermon ON resource(sermon_id);
CREATE INDEX idx_bible_sermon ON bible_reference(sermon_id);

CREATE INDEX idx_relation_sermon ON sermon_relation(sermon_id);
CREATE INDEX idx_relation_related ON sermon_relation(related_sermon_id);

