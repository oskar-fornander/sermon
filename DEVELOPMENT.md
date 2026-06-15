# Sermon - Utvecklarguide och Systemarkitektur

Detta dokument är avsett för utveckling och underhåll av **sermon**-applikationen. Det ger en teknisk överblick över arkitekturen, filstrukturen och databasdesignen.

---

## Projektets arkitektur

Sermon är uppdelat i fyra logiska lager:

1.  **CLI-lager (`app/cli.py` & `app/commands/`):** Byggt med `Typer`. Hanterar kommandoradsparametrar, flaggor och dirigerar anrop till rätt service.
2.  **Service-lager (`app/services/`):** Innehåller affärslogiken. Här sker validering av indata, orkestrering av databasoperationer, filhantering (t.ex. radering till papperskorgen med `send2trash`) och nätverksanrop (t.ex. SFTP-uppladdning).
3.  **Databaslager (`app/db.py`):** Innehåller alla SQL-frågor mot SQLite-databasen. Sköter transaktioner (`with conn:`) och mappning till dataclasses.
4.  **Presentationslager (`app/presentation/`):** Byggt med `Rich`. Hanterar all formatering för terminalen (paneler, färger, tabeller, validerande promptar).

### Mappningsmönster: `SermonDraft`
Vid skapande (`new`) och redigering (`edit`) läses data först ut från databasen och konverteras till ett `SermonDraft`-objekt (definierat i `app/services/sermon_draft.py`). Alla ändringar görs mot detta objekt i minnet. Först när användaren väljer att spara (`s`) valideras objektet och skrivs till databasen i en och samma transaktion.

---

## Komplett filstruktur

Nedan visas hur kodprojektet och arkivmappen är uppbyggda.

```
predikan/                         # Överordnad mapp
│
├── sermon/                       # Källkod (versionshanterad i Git)
│   ├── app/
│   │   ├── cli.py                # CLI Entrypoint och Typer-definitioner
│   │   ├── config.py             # Initiering av miljö och sökvägar
│   │   ├── db.py                 # Databasfrågor och transaktioner
│   │   ├── errors.py             # Applikationsspecifika exceptions
│   │   ├── utils.py              # Diverse hjälpfunktioner (datum, fil-länkar, mp3-meta)
│   │   │
│   │   ├── commands/             # CLI-kommandon (ett per fil/subtyper)
│   │   │   ├── backup.py
│   │   │   ├── delete.py
│   │   │   ├── edit.py
│   │   │   ├── export.py
│   │   │   ├── files.py
│   │   │   ├── list.py
│   │   │   ├── new.py
│   │   │   ├── open.py
│   │   │   ├── podcast.py
│   │   │   ├── search.py
│   │   │   └── show.py
│   │   │
│   │   ├── presentation/         # Terminalformatering med Rich
│   │   │   ├── common.py         # Paneler, inputs och bekräftelser
│   │   │   ├── edit_sermon.py    # Interaktiva menyer för editering
│   │   │   ├── new_sermon.py     # Presentation för nyskapande
│   │   │   ├── sermon_card.py    # Kortvy över en predikan (show/preview)
│   │   │   ├── sermon_list.py    # Tabellpresentation för sök/list
│   │   │   └── theme.py          # Färgschema och Rich-teman
│   │   │
│   │   ├── services/             # Affärslogik
│   │   │   ├── delete_sermon.py  # Raderingsflöde och trash-backuper
│   │   │   ├── edit_sermon.py    # Kontrollflöde för editering
│   │   │   ├── export_html.py    # HTML-rendering och sFTP-uppladdning
│   │   │   ├── list_sermons.py   # Logik för listning och filter
│   │   │   ├── new_sermon.py     # Flöde för nyskapande av predikan
│   │   │   ├── open.py           # Logik för att starta externa macOS-appar
│   │   │   ├── podcast.py        # RSS-generering, MP3-storlekar, podcast-pruning
│   │   │   ├── search_sermons.py # Sökflöde med interaktiv granskning
│   │   │   ├── sermon_draft.py   # Dataklasser för SermonDraft och validering
│   │   │   └── upload.py         # SCP/SSH-anrop för SFTP
│   │   │
│   │   ├── templates/            # Mallar för export
│   │   │   ├── podcast.xml.j2    # Jinja2-mall för podcast RSS
│   │   │   ├── sermon.css        # CSS för mobilöversikt
│   │   │   ├── sermon.html.j2    # Jinja2-mall för mobilöversikt
│   │   │   └── sermon.js         # Debouncerad klientsökning och sortering
│   │   │
│   │   └── tools/                # Hjälpverktyg
│   │       ├── files.py          # Disk vs databas-analys (check_files)
│   │       └── import_xml.py     # Engångsskript för XML-import
│   │
│   ├── pyproject.toml            # App-metadata, dependencies och script entrypoints
│   ├── requirements.txt          # Python-paketlista (för pip)
│   ├── schema.sql                # SQLite-databasschema
│   ├── uv.lock                   # Låst dependency-träd för uv
│   └── README.md                 # Användardokumentation
│
└── archive/                      # Predikoarkiv (synkas via t.ex. Mega)
    ├── data/
    │   ├── sermons.db            # Den aktiva SQLite-databasen
    │   └── backup/               # Säkerhetskopior genererade av `sermon backup`
    │
    ├── files/
    │   ├── manuscripts/          # PDF-manuskript (t.ex. P371.pdf)
    │   ├── recordings/           # Ljudfiler i MP3-format
    │   └── resources/            # Övrigt extramaterial
    │
    └── html/
        └── index.html            # Den senast genererade mobilöversikten
```

---

## Databasdesign (SQLite)

Databasen använder `FOREIGN KEY`s med `ON DELETE CASCADE` för att förhindra föräldralösa rader i relaterade tabeller när en predikan tas bort.


### Tabeller och Index
Alla index skapas automatiskt av `ensure_database()` i `app/config.py` med SQL från `schema.sql`. Det finns index på alla främmande nycklar (`sermon_id`) för att optimera `JOIN`-operationer vid sökning och listning.

---

## Utvecklingsinstruktioner

### Lägga till ett nytt kommando
1.  Skapa kommandofilen i `app/commands/[kommando_namn].py` med `typer.Typer()`.
2.  Registrera kommandot i `app/cli.py`:
    *   Importera modulen.
    *   Lägg till namnet i `COMMAND_ORDER` för att styra var det visas i `--help`.
    *   Lägg till det i `app.add_typer()` eller `app.command()`.

### Valideringsregler
All validering sker i `validate_sermon_draft` i `app/services/sermon_draft.py`. Regex-mönster för giltiga filnamn och koder finns samlade i `PATTERN`-konstanten i `app/utils.py`. Om du ändrar ett filnamnsformat, se till att uppdatera motsvarande regex där.
