-- schema.sql for sermon.db

CREATE TABLE sermon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    context TEXT,
    introduction TEXT,
    message TEXT,
    notes TEXT
);

CREATE TABLE service (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    place TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (sermon_id) REFERENCES sermon(id)
);

CREATE TABLE manuscript (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    version INTEGER,
    date TEXT,
    notes TEXT,
    FOREIGN KEY (sermon_id) REFERENCES sermon(id),
    UNIQUE (sermon_id, file_name)
);

CREATE TABLE recording (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    date TEXT NOT NULL,
    file_name TEXT,
    external_url TEXT,
    notes TEXT,
    FOREIGN KEY (sermon_id) REFERENCES sermon(id)
);

CREATE TABLE resource (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    title TEXT,
    notes TEXT,
    FOREIGN KEY (sermon_id) REFERENCES sermon(id)
);

CREATE TABLE bible_reference (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id INTEGER NOT NULL,
    reference_text TEXT NOT NULL,
    FOREIGN KEY (sermon_id) REFERENCES sermon(id)
);

CREATE INDEX idx_service_sermon ON service(sermon_id);
CREATE INDEX idx_manuscript_sermon ON manuscript(sermon_id);
CREATE INDEX idx_recording_sermon ON recording(sermon_id);
CREATE INDEX idx_resource_sermon ON resource(sermon_id);
CREATE INDEX idx_bible_sermon ON bible_reference(sermon_id);
