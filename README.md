# Sermons

*Oskar Fornander*

Privat predikoregister för mina predikningar.


## Mappstruktur:
````
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
````

## CLI Commands
```
* sermon new                    #Add new sermon
* sermon list                   #Show (all) sermons in a list
* sermon show P371              #Show particular sermon by ID
* sermon search joh             #Search and list sermons by ...
* sermon add-service P371       #Add a new service to an existing sermon
    * sermon attach-manuscript P371 #Add a manuscript to a sermon
    * sermon attach-recording P371  #Add a recording to a sermon
* sermon export html            #Create a html overview of all sermons, to browse in mobile
```

