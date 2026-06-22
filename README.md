# Sermon - Predikoarkiv
*© Oskar Fornander 2026*

**Sermon** är ett terminalbaserat verktyg (CLI) skrivet i Python för att organisera, söka i och underhålla ett personligt predikoregister. Det hanterar metadata om predikningar, såsom bibelreferenser, sammanhang, omdömen, manuskript och inspelningar – i en säker, lokal databas på din dator. Dessutom länkas till tillhörande manus (PDF), ljud-/ och filminspelningar (MP3/MP4), resurser och relaterade predikningar.

Med enkla kommandon i terminalen kan du söka efter bibelord, öppna tillhörande PDF-manus eller ljudfiler direkt i dina favoritprogram, samt köra hälsokontroller av dina arkivfiler. Verktyget har dessutom inbyggt stöd för att exportera registret till en sökbar, mobilvänlig webbsida samt generera ett podcast-flöde (RSS) som laddas upp till din server via SFTP med en enkel knapptryckning.

Sermon är ett fritt och öppet verktyg för hantering av predikoregister, utvecklat av Oskar Fornander. Läs mer nedan om verktyget och hur du installerar.

---

## Funktioner i korthet

*   **Översikt & Sök:** Visa all data om en predikan, sök på fritext eller bibelreferenser, samt lista predikningar sorterat efter datum eller predikokod.
*   **Interaktiv inmatning & redigering:** Skapa nya eller uppdatera befintliga predikningar med en kraftfull terminalbaserad redigerare för både metadata och kopplade filer.
*   **Filhantering:** Öppna tillhörande manus, inspelningar eller resurser direkt från terminalen med dina förvalda program.
*   **Hälsokontroll av filer:** Hitta saknade filer som refereras i databasen, samt oanvända filer som ligger i dina arkivmappar.
*   **HTML-export:** Generera en sökbar, mobilvänlig HTML-sida över hela registret och ladda upp den automatiskt via SFTP.
*   **Podcast-publicering:** Exportera predikningar till en podcast-feed (RSS) och ladda upp ljudfiler och XML direkt till din server.

---

## Installation

Sermon kräver **Python 3.12 eller senare** installerat på datorn.

### Rekommenderad installation: `uv`

```bash
uv tool install git+https://github.com/oskar-fornander/sermon.git
```

Du kan sedan köra programmet från valfri katalog med: `sermon`

För att uppdatera till senaste version: 
```bash
uv tool upgrade sermon
```

För att avinstallera:
```bash
uv tool uninstall sermon
```

### Alternativ installation: `pipx`

```bash
pipx install git+https://github.com/oskar-fornander/sermon.git
```

Du kan sedan köra programmet från valfri katalog med: `sermon`

För att uppdatera till senaste version: 
```bash
pipx upgrade sermon
```

För att avinstallera:
```bash
pipx uninstall sermon
```

## Konfiguration

Första gången du kör programmet skapas en standardkonfiguration i:
`~/.config/sermon/config.yaml`

Öppna den filen för att konfigurera sökvägar till ditt predikoarkiv samt SFTP-uppgifter.

### Inställningar i `config.yaml`

| Inställning | Beskrivning | Exempel / Standardvärde |
| :--- | :--- | :--- |
| `user` | Ditt namn. Används för att personifiera hjälprutor samt som skapare i webbexporten och podcast-flödet. | `"Oskar Fornander"` |
| `archive_path` | Den lokala sökvägen till mappen där alla predikofiler, backuper och databasen lagras. | `"~/predikan/archive"` |
| **`cloud:`** | *Inställningar för att integrera med din lokala molnsynk (t.ex. MEGA, Dropbox).* | |
| `  provider` | Namnet på molntjänsten som synkar din lokala arkivmapp. | `"MEGA"` |
| `  urls.manuscripts` | Delningslänk till din manuskript-mapp i molnet (används för klickbara länkar i webbexporten). | `"https://mega.nz/..."` |
| `  urls.recordings` | Delningslänk till din inspelnings-mapp i molnet. | `"https://mega.nz/..."` |
| `  urls.resources` | Delningslänk till din resurs-mapp i molnet. | `"https://mega.nz/..."` |
| **`apps:`** | *Programnamn som ska användas för att öppna filer. Lämna tomma `""` för systemets standardprogram.* | |
| `  pdf` | Program för att öppna PDF-manuskript. | `"Preview"` (macOS) |
| `  audio` | Program för att spela upp ljudinspelningar (MP3). | `"QuickTime Player"` (macOS) |
| `  video` | Program för att spela upp videoinspelningar (MP4). | `"QuickTime Player"` (macOS) |
| `  browser` | Webbläsare för att öppna länkar. | `"Safari"` (macOS) |
| **`web:`** | *Hemsidesinställningar* | |
| `  url` | Den publika webbadressen där din predikolista och podcast kommer att ligga. | `"https://exempel.se/predikan"` |
| **`sftp:`** | *Anslutningsuppgifter för automatisk uppladdning av hemsida och podcast via SFTP.* | |
| `  root` | Sökvägen till din användares hemkatalog eller webb-root på fjärrservern. | `"/var/www/html"` |
| `  host` | Fjärrserverns värdnamn eller IP-adress. | `"sftp.exempel.se"` |
| `  port` | SSH/SFTP-port. | `22` |
| `  username` | Ditt SSH-användarnamn på servern. | `"mitt_anvandarnamn"` |
| `  key_file` | Sökväg till din privata SSH-nyckel för lösenordslös inloggning. | `"~/.ssh/id_ed25519"` |
| **`html:`** | *Inställningar för den sökbara webböversikten.* | |
| `  remote_dir` | Mapp på fjärrservern (relativt till sftp-root) dit webbsidan laddas upp. | `"public_html"` |
| **`podcast:`** | *Inställningar för RSS-feed och ljudfiler för podden.* | |
| `  remote_dir` | Mapp på fjärrservern (relativt till sftp-root) dit ljudfiler och RSS-feed laddas upp. | `"public_html/podcast"` |
| `  cover_image` | Filnamn för omslagsbilden till din podcast (måste finnas i din podcast-arkivmapp). | `"cover.jpg"` |
| `  title` | Podcastens namn i podcast-spelare. | `"Predikningar"` |
| `  description` | En kort beskrivning av podcasten. | `"En samling predikningar av..."` |
| `  author` | Podcastens skapare/talare. | `"Oskar Fornander"` |
| `  min_episodes` | Minsta antal avsnitt som alltid sparas i RSS-flödet (även om de blivit för gamla). | `3` |
| `  max_days` | Maxålder i dagar för att behålla ett avsnitt i RSS-flödet (äldre gallras automatiskt bort). | `60` |


---

### Förutsättning för SFTP-uppladdning:

För att kunna ladda upp html-sida av predikoregistret och podcast-filer till en server krävs att systemverktyget `scp` är installerat och tillgängligt i din terminal (i systemets sökväg/PATH).
* **macOS och Linux:** Detta är installerat som standard och kräver ingen åtgärd.
* **Windows:** Verktyget ingår i funktionen *OpenSSH-klient* (vilket är aktiverat som standard i moderna versioner av Windows 10 och 11).


## Användning

Kör `sermon --help` för en fullständig överblick över alla tillgängliga kommandon.

### Söka och lista
```bash
# Lista de 10 senaste predikningarna (standardsortering efter kod)
sermon list

# Visa alla predikningar sorterade efter datum (nyast först)
sermon list --all --sort date

# Sök efter predikningar som innehåller ordet "nåd" och "tro"
sermon search nåd tro

# Sök endast i bibelreferenser
sermon search "Joh 3" --bible
```

### Visa, skapa och redigera
```bash
# Visa en specifik predikan snyggt uppställd
sermon show P371

# Skapa en ny predikan interaktivt (frågar efter kod och titel, öppnar sedan redigeringsmenyn)
sermon new

# Redigera en befintlig predikan interaktivt
sermon edit P371
```

### Hantera filer
Sermon kan öppna de fysiska filerna associerade med en predikan:
```bash
# Öppna manus (PDF)
sermon open manuscript P371

# Öppna ljud- eller videoinspelning
sermon open recording P371

# Kontrollera diskfiler mot databasen (hitta oanvända eller saknade PDF/MP3-filer)
sermon files check
```

### Export & Underhåll
```bash
# Skapa lokalt och ladda upp index.html-sidan via SFTP
sermon export html

# Publicera en specifik predikan (eller godtycklig MP3-fil) till podcast-flödet
sermon export podcast P371

# Visa och hantera avsnitt i podcast
sermon podcast list

# Säkerhetskopiera SQLite-databasen till data/backup/
sermon backup

# Radera en predikan och flytta dess tillhörande PDF- och MP3-filer till papperskorgen
sermon delete P371
```

## Licens

Sermon är fri programvara och distribueras under MIT-licensen. Projektet utvecklades ursprungligen för mitt eget predikoarkiv, men om det kan hjälpa andra predikanter eller församlingar är det en stor glädje. Förslag, felrapporter och förbättringar välkomnas.
