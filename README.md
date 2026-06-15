# Sermon - Predikoarkiv
*© Oskar Fornander 2026*

Sermon är ett terminalbaserat verktyg (CLI) skrivet i Python för att organisera, söka i och underhålla ett personligt predikoregister. Det hanterar metadata om predikningar (rubrik, sammanhang, bibelreferenser, budskap, kommentarer, datum och platser) samt länkar till tillhörande manus (PDF), ljud-/ och filminspelningar (MP3/MP4), resurser och relaterade predikningar.

---

## Funktioner i korthet

*   **Översikt & Sök:** Sök på fritext eller bibelreferenser, samt lista predikningar sorterat efter datum eller predikokod.
*   **Interaktiv inmatning & redigering:** Skapa nya eller uppdatera befintliga predikningar med en kraftfull terminalbaserad redigerare för både metadata och kopplade filer.
*   **Filhantering:** Öppna tillhörande manus, inspelningar eller resurser direkt från terminalen med dina förvalda program.
*   **Hälsokontroll av filer:** Hitta saknade filer som refereras i databasen, samt oanvända filer som ligger i dina arkivmappar.
*   **HTML-export:** Generera en sökbar, mobilvänlig HTML-sida över hela registret och ladda upp den automatiskt via SFTP.
*   **Podcast-publicering:** Exportera predikningar till en podcast-feed (RSS) och ladda upp ljudfiler och XML direkt till din server.

---

## Installation & Setup

Sermon kräver Python 3.12 eller senare.

### Alternativ 1: Installation med `uv` (rekommenderas)
Om du använder pakethanteraren `uv` kan du synka och installera verktyget i redigerbart läge (editable) globalt:

```bash
# Synka dependencies (skapar/uppdaterar uv.lock)
uv sync

# Installera verktyget globalt i redigerbart läge
uv tool install --editable .
```
Du kan sedan köra appen direkt med kommandot `sermon`. Om du vill köra koden utan att installera den globalt använder du:
```bash
uv run sermon [kommando]
```

### Alternativ 2: Installation med standard `venv` och `pip`
```bash
# Skapa virtuell miljö
python -m venv .venv

# Aktivera virtuell miljö (macOS/Linux)
source .venv/bin/activate

# Installera projektet i redigerbart läge
pip install -e .
```

---

## Konfiguration

Första gången du kör appen skapas en standardkonfiguration i:
`~/.config/sermon/config.yaml`

Öppna den filen för att konfigurera sökvägar till ditt predikoarkiv samt SFTP-uppgifter.

### Exempel på `config.yaml`
```yaml
user: Oskar Fornander
root: ~/predikan/archive                # Mappen där databasen och filerna ligger
database: sermon.db
paths:
  database: data
  backup: data/backup
  manuscripts: files/manuscripts
  recordings: files/recordings
  resources: files/resources
  html: html
  podcast: podcast
cloud:
  provider: Mega                        # Namn på din molntjänst (Google Drive, Mega, etc.)
  urls:
    manuscripts: "https://mega.nz/..."
    recordings: "https://mega.nz/..."
    resources: "https://mega.nz/..."
apps:                                   # Program som öppnar dina filer på macOS
  pdf: Preview
  audio: QuickTime Player
  video: QuickTime Player
  browser: Safari
sftp:                                   # Inställningar för uppladdning av HTML/podcast
  host: din.server.se
  port: 22
  username: sftp_användare
  key_file: ~/.ssh/id_rsa
web:
  site_url: "https://dinhemsida.se"
  site_root: "/var/www/sermon"
html:
  remote_dir: "html"
podcast:
  remote_dir: "podcast"
  feed_file: "feed.xml"
  audio_path: "audio"
  cover_image: "cover.jpg"
  title: "Predikokanalen"
  description: "Predikningar av Oskar Fornander"
  author: "Oskar Fornander"
  min_episodes: 3
  max_days: 60
```

---

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
