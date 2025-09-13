# ProtoNord Backup System

Dette systemet sørger for automatisk backup av ProtoNord-nettsiden til både Google Drive og Jottacloud.

## 🔧 Oppsett

### Forutsetninger
- `rclone` installert og konfigurert
- Tilgang til Google Drive og Jottacloud gjennom rclone
- Crontab for automatisk kjøring

### Installer og konfigurer rclone
```bash
# Installer rclone
curl https://rclone.org/install.sh | sudo bash

# Konfigurer Google Drive
rclone config

# Konfigurer Jottacloud
rclone config
```

## 📁 Backup-struktur

### GFS (Grandfather-Father-Son) Rotasjon
- **Daily**: Daglige backuper (beholder 30 dager)
- **Weekly**: Ukentlige backuper (søndager)
- **Monthly**: Månedlige backuper (1. i måneden)

### Mappestruktur i cloud
```
ProtoNordBackup/
├── 2025/
│   ├── 01/
│   │   ├── 01/          # Daily backuper
│   │   └── monthly/     # Månedlig backup
│   ├── Week_01/         # Ukentlig backup
│   └── Week_02/
```

## 🚀 Bruk

### Manuell backup
```bash
# Kjør backup nå
./scripts/protonord_cloud_backup.sh
```

### Automatisk backup med cron
```bash
# Rediger crontab
crontab -e

# Legg til daglig backup kl 02:00
0 2 * * * /home/kau005/project-lifecycle-manager/scripts/protonord_cloud_backup.sh

# Eller ukentlig backup (søndager kl 03:00)
0 3 * * 0 /home/kau005/project-lifecycle-manager/scripts/protonord_cloud_backup.sh
```

## 📦 Hva backupes

### Inkludert i backup
- ✅ Full kildekode (React komponenter, CSS, etc.)
- ✅ Shopify data-filer
- ✅ Statiske ressurser (bilder, logo)
- ✅ Konfigurasjonsfiler (package.json, docusaurus.config.js)
- ✅ Dokumentasjon
- ✅ Git historie og metadata
- ✅ Build-scripts og automation

### Ekskludert fra backup
- ❌ `node_modules/` (kan gjenopprettes med npm install)
- ❌ `.git/` store filer (Git LFS)
- ❌ Temp-filer og caches

## 🔄 Gjenoppretting

### Last ned fra cloud
```bash
# List tilgjengelige backuper
rclone ls gdrive:ProtoNordBackup/2025/

# Last ned spesifikk backup
rclone copy gdrive:ProtoNordBackup/2025/01/15/protonord-website_20250115_120000.tar.gz ./

# Pakk ut backup
tar -xzf protonord-website_20250115_120000.tar.gz
```

### Gjenopprett website
```bash
cd project-lifecycle-manager/
npm install
npm start
```

## 📊 Logging

Alle backup-operasjoner logges til:
- `~/protonord_backup.log`

### Sjekk backup-status
```bash
# Se siste backup-kjøringer
tail -50 ~/protonord_backup.log

# Sjekk for feil
grep "FEIL\|ERROR" ~/protonord_backup.log
```

## 🔐 Sikkerhet

- Backup-filene inneholder **ikke** sensitive API-nøkler
- Shopify API-nøkler lagres kun lokalt i environment variabler
- rclone-konfigurasjon er beskyttet med filrettigheter (600)

## 🛠 Feilsøking

### Vanlige problemer

#### rclone authentication feil
```bash
# Test rclone tilkobling
rclone lsd gdrive:
rclone lsd jottacloud:

# Refresh tokens
rclone config reconnect gdrive:
rclone config reconnect jottacloud:
```

#### Backup feiler
```bash
# Sjekk disk-plass
df -h

# Sjekk rclone konfigurasjon
rclone config show

# Test manuell backup
./scripts/protonord_cloud_backup.sh
```

#### Store filer
```bash
# Sjekk backup-størrelse
du -sh /tmp/protonord_backup_temp/

# Eksluder store filer ved behov
# (redigér scriptet for å legg til --exclude parametere)
```

## 📈 Overvåking

### Cron email notifikasjoner
```bash
# Legg til i crontab for email-varsler ved feil
MAILTO=din@email.com
0 2 * * * /home/kau005/project-lifecycle-manager/scripts/protonord_cloud_backup.sh || echo "Backup feilet!" | mail -s "ProtoNord Backup Feil" $MAILTO
```

### Automated testing
Scriptet inkluderer automatisk validering av:
- Kildemapper eksisterer
- rclone er installert og konfigurert
- Backup-filer opprettes korrekt
- Upload til begge cloud-tjenester

## 📅 Vedlikehold

### Månedlig oppgaver
- [ ] Sjekk backup-logger for feil
- [ ] Verifiser at gamle backuper slettes automatisk
- [ ] Test gjenoppretting av en tilfeldig backup
- [ ] Sjekk cloud storage-kvote

### Årlig oppgaver
- [ ] Oppdater rclone til nyeste versjon
- [ ] Gjennomgå backup retention policy
- [ ] Test fullstendig disaster recovery