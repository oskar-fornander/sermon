# Sermons

*Oskar Fornander*

Privat predikoregister för mina predikningar.


## Mappstruktur:
sermons/
├── app/
│   ├── cli.py
│   ├── db.py
│   ├── models.py
│   ├── commands/
│   │   ├── new.py
│   │   ├── list.py
│   │   ├── show.py
│   │   ├── search.py
│   │   ├── service.py
│   │   └── export.py
│
├── data/
│   └── sermons.db        # SQLite
│
├── files/
│   ├── manuscripts/      # PDF
│   ├── recordings/       # MP3
│   └── resources/
│
├── html/
│   └── index.html        # Mobil översikt
│
├── tools/
│   └── import_xml.py     # engångsskript
│
├── README.md
