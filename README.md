# Sermons

*Oskar Fornander*

Privat predikoregister för mina predikningar.

## TODO

- importera befintlig databas i nya systemet
- funktion för backup?
- sökfunktion
- podcast-funktion?
- skapa databas ifall ingen finns vid start?
- ...
- 


## Mappstruktur
Överblick: 
```
predikan            # överordnad mapp
├── sermon/         # koden - synkas med git
└── archive/        # filerna - synkas med molntjänst
```
Fullständig mappstruktur:
```
predikan/                   # överordnad mapp
├── sermon/                 # CLI-projekt (GitHub)
│   ├── app/                # Alla python-filer
│   │   ├── cli.py          
│   │   ├── db.py
│   │   ├── models.py
│   │   └── commands/       # Varje CLI-kommando har en egen fil
│   │       ├── show.py
│   │       ├── list.py
│   │       ├── search.py
│   │       ├── new.py
│   │       ├── attach.py
│   │       ├── edit.py
│   │       └── export.py
│   │
│   ├── tools/
│   │   └── import_xml.py     # engångsskript för import från gammalt system
│   │
│   ├── schema.sql            # Schema för databasen
│   ├── config.yaml           # Konfigurationsfil
│   ├── requirements.txt      
│   └── README.md
│
└── archive/                  # filer (molntjänst)
    ├── data/
    │   └── sermons.db        # SQLite
    │
    ├── files/
    │   ├── manuscripts/      # PDF
    │   ├── recordings/       # MP3
    │   └── resources/        # PDF etc.
    │
    └── html/
        └── index.html        # Mobil översikt
```

All kod ligger i mappen `sermon/` och synkas med Git.
Alla filer ligger i mappen `archive/` som synkas med valfri *molntjänst*.

## Molntjänst

Synkning av mappen `archive/`sker med valfri molntjänst. Denna är inte beroende av koden i `sermon/`och kan därför bytas ut när som helst.

Använd förslagsvis *Google Drive*, *pCloud* eller *Mega*. Synkningen behöver ske automatiskt och gärna så att data sparas i molnet och syns på datorn utan att ta upp plats, men kan öppnas från datorn (laddas ned när en fil öppnas). Utrymmet behöver vara tillräckligt stort (uppskattningsvis >10GB till att börja med). Synkning till flera datorer. Notera att molntjänsten måste funka på de operativsystem och versioner som används.

Start: **Mega**

## Databas

```
sermon
 ├── service
 ├── manuscript
 ├── recording
 ├── resource
 └── bible_reference
```

Alla relationer är: enkelriktade, icke-cirkulära och lätta att fråga i SQLite.

### Tabeller

```
Sermon: id, title, context, introduction, message, notes
Service: id, sermon_id, date, place, notes
Manuscript: id, sermon_id, file_name, version, date, notes
Recording: id, sermon_id, type, file_name, external_url, date, notes
Resource: id, sermon_id, file_name, title, notes
Bible_reference: id, sermon_id, reference_text
```

*Bible_reference* är möjligt att utveckla senare, men i nuläget sparas varje inmatad bibelreferens som en egen rad, så som den skrevs. t.ex. `sermon attach bible "Joh 1:1-5; Joh 8:12; 1Mos 1:1-3"` –> 3 referenser


## CLI Commands
```
* sermon show P371              #Show particular sermon by ID
* sermon list                   #Show (all) sermons in a list
* sermon search joh             #Search and list sermons by ...
* sermon new                    #Add new sermon [id, title, context, reference(s), introduction, message, (related), comment, report]
* sermon delete P371            #Delete a post
* sermon edit                   #Edit an existing sermon, its meta data and links and connected resources
* sermon export html            #Create a html overview of all sermons, to browse in mobile
* sermon export podcast         #Export sermon for podcast
```

## Old XML-element
```
  <sermon index="P370" title="Messias" context="F&#xF6;rsta s&#xF6;ndagen i advent">
    <reference>Sak 9:9-10</reference>
    <introduction>&#x201D;Se, din konung kommer till dig&#x201D;; den som kommer &#xE4;r Messias man v&#xE4;ntat p&#xE5;.</introduction>
    <message>Jesus f&#xE5;r b&#xE4;ra alla f&#xF6;rv&#xE4;ntningar p&#xE5; den v&#xE4;ntade messias/kungen. Mycket i evangelierna pekar p&#xE5; att han ses som den messias man v&#xE4;ntat p&#xE5;.</message>
    <keyword/>
    <related/>
    <service date="2025-11-30" place="Missionskyrkan, Lagan" notice=""/>
    <manuscript>P370.pdf</manuscript>
    <resource title=""/>
    <recording type="audio" date="2025-11-30">2025-11-30_Predikan.mp3</recording>
    <comment/>
    <report>B</report>
  </sermon>
````
