# Sermons

*Oskar Fornander*

Privat predikoregister för mina predikningar.


## Mappstruktur
````
sermons/
├── app/
│   ├── cli.py
│   ├── db.py
│   ├── models.py
│   └── commands/
│       ├── show.py
│       ├── list.py
│       ├── search.py
│       ├── new.py
│       ├── attach.py
│       ├── edit.py
│       └── export.py
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
└── README.md
````

## CLI Commands
```
* sermon show P371              #Show particular sermon by ID
* sermon list                   #Show (all) sermons in a list
* sermon search joh             #Search and list sermons by ...
* sermon new                    #Add new sermon [id, title, context, reference(s), introduction, message, (related), comment, report]
    * sermon attach service P371    #Add a new service to an existing sermon [date, place, notice on service]
    * sermon attach manuscript P371 #Add a manuscript to a sermon [file name]
    * sermon attach recording P371  #Add a recording to a sermon [date, type, link/file name]
    * sermon attach resource P371   #Add a resource to a sermon [file name]
* sermon delete P371            #Delete a post
* sermon edit                   #Edit an existing sermon, its meta data and links
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
