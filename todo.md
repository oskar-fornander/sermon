# TODO


Vad vi gör härnäst (rekommenderad ordning)

1 Skapa data/sermons.db

2 Skriva db.py

3 init_db()

4 get_connection()

5 Implementera new

6 Implementera list all

7 Implementera show

8 Vi börjar enkelt men rätt.


👉 Relationerna är enkelriktade

* service vet vilken sermon den hör till

* sermon “vet inte” om sina services förrän du frågar databasen

Är relationerna ömsesidiga? Nej – och det är bra. service pekar på sermon sermon är “okunnig” tills du frågar Relationer uppstår vid fråga, inte vid lagring.

I relationsdatabaser är det god praxis att: varje rad har ett primärnyckel-id även om du själv aldrig “ser” eller bryr dig om det


CREATE TABLE sermon (
    id TEXT PRIMARY KEY,          -- P371
    title TEXT NOT NULL,
    context TEXT,                 -- Juldagen, Fastan etc
    introduction TEXT,
    message TEXT,
    notes TEXT,
);

CREATE TABLE service (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id TEXT NOT NULL,
    date DATE NOT NULL,
    place TEXT,
    notice TEXT,
    FOREIGN KEY (sermon_id) REFERENCES sermon(id)
);

CREATE TABLE manuscript (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    version TEXT,
    created_at DATE,
    FOREIGN KEY (sermon_id) REFERENCES sermon(id)
);

CREATE TABLE recording (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sermon_id TEXT NOT NULL,
    service_id INTEGER,
    kind TEXT NOT NULL,          -- 'audio', 'video'
    filename TEXT,               -- om lokal fil
    url TEXT,                    -- om extern (YouTube)
    FOREIGN KEY (sermon_id) REFERENCES sermon(id),
    FOREIGN KEY (service_id) REFERENCES service(id)
);

Regler i koden (inte DB): minst filename ELLER url måste finnas, CLI kan validera detta


CREATE TABLE bible_reference (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference TEXT NOT NULL UNIQUE
);

CREATE TABLE sermon_bible_reference (
    sermon_id TEXT NOT NULL,
    bible_reference_id INTEGER NOT NULL,
    PRIMARY KEY (sermon_id, bible_reference_id),
    FOREIGN KEY (sermon_id) REFERENCES sermon(id),
    FOREIGN KEY (bible_reference_id) REFERENCES bible_reference(id)
);
