# 🚀 ProtoNord Automatisk Cloud Synkronisering

Dette systemet synkroniserer automatisk filer fra **ProtoNord** mapper i Jottacloud og Google Drive til Docusaurus wikien.

## 📋 Oversikt

### 🔄 Automatisk Synkronisering
- **Kjører**: Hver natt kl 02:00
- **Kilde**: `jottacloud:protonord/` og `gdrive:protonord/` mapper
- **Mål**: `static/data/protonord_cloud_data.json`
- **Restart**: Docusaurus restartes automatisk etter sync

### 🛠 Komponenter

```
scripts/
├── automated_protonord_sync.py    # Hovedscript for automatisk sync
├── protonord_sync.py             # Manuelt sync script  
├── setup_cron.sh                 # Setup av cron job
└── sync_dashboard.py             # Status dashboard

config/
└── sync_config.ini               # Konfigurasjon (fremtidig bruk)

logs/
├── protonord_sync_YYYY-MM-DD.log # Daglige sync logs
└── cron.log                      # Cron output
```

## 🚀 Kom i gang

### 1. Setup Automatisk Synkronisering
```bash
cd /home/kau005/project-lifecycle-manager
./scripts/setup_cron.sh
```

### 2. Sjekk Status
```bash
python3 scripts/sync_dashboard.py
```

### 3. Manuell Synkronisering
```bash
python3 scripts/automated_protonord_sync.py
```

## 📊 Dashboard Kommandoer

| Kommando | Beskrivelse |
|----------|-------------|
| `python3 scripts/sync_dashboard.py` | Vis sync status |
| `python3 scripts/automated_protonord_sync.py` | Manuell sync |
| `crontab -l` | Se cron jobs |
| `tail -f logs/cron.log` | Se cron logs live |
| `ls -la logs/` | Liste alle logs |

## 🔧 Konfigurasjon

### Endre Sync Tidspunkt
```bash
crontab -e
# Rediger linjen: 0 2 * * * ...
# Format: min time dag måned ukedag
```

### Cron Eksempler
- `0 2 * * *` - Hver dag kl 02:00
- `0 */6 * * *` - Hver 6. time  
- `0 2 * * 1` - Hver mandag kl 02:00
- `*/30 * * * *` - Hver 30. minutt

## 📁 Cloud Struktur

### Påkrevd Mappestruktur
```
jottacloud:protonord/          # Jottacloud ProtoNord mapper
gdrive:protonord/              # Google Drive ProtoNord mapper
```

### Støttede Filtyper
- Alle filtyper synkroniseres
- Metadata inkluderer: navn, størrelse, endringsdato
- Mappehierarkiet bevares

## 🔍 Logging

### Log Filer
- **Daglige logs**: `logs/protonord_sync_YYYY-MM-DD.log`
- **Cron output**: `logs/cron.log`
- **Retention**: 30 dager (automatisk sletting)

### Log Nivåer
- `INFO`: Normal operasjon
- `WARNING`: Advarsler
- `ERROR`: Feil som krever oppmerksomhet

## 🔧 Feilsøking

### Vanlige Problemer

#### Cron Job Kjører Ikke
```bash
# Sjekk cron service
sudo systemctl status cron

# Se cron logs
tail -f /var/log/syslog | grep CRON
```

#### rclone Feil
```bash
# Test rclone manuelt
rclone lsjson jottacloud:protonord
rclone lsjson gdrive:protonord

# Sjekk rclone config
rclone config show
```

#### Docusaurus Restart Feil
```bash
# Manuell restart
pkill -f "docusaurus start --port 3001"
cd /home/kau005/project-lifecycle-manager
nohup npm start > logs/docusaurus.log 2>&1 &
```

### Debug Mode
```bash
# Kjør med detaljert logging
python3 scripts/automated_protonord_sync.py --debug
```

## 📈 Overvåking

### Status Dashboard
Kjør dashboard for live status:
```bash
python3 scripts/sync_dashboard.py
```

Viser:
- ⏰ Siste synkronisering
- 📁 Antall filer per cloud
- 🕒 Cron status (aktiv/inaktiv)
- 📋 Siste log entries

### Automatisk Varsling
Konfigurasjon for fremtidig implementering:
- E-post ved sync feil
- Webhook notifikasjoner
- Slack/Teams integrasjon

## 🔄 Vedlikehold

### Månedlig Sjekkliste
- [ ] Sjekk sync status: `python3 scripts/sync_dashboard.py`
- [ ] Se gjennom error logs: `grep ERROR logs/*.log`
- [ ] Teste manuell sync: `python3 scripts/automated_protonord_sync.py`
- [ ] Sjekk disk space: `df -h`

### Backup
Cron backup lages automatisk ved setup:
```bash
ls logs/crontab_backup_*
```

## 📞 Support

### Ved Problemer
1. Sjekk dashboard: `python3 scripts/sync_dashboard.py`
2. Se siste logs: `tail -20 logs/protonord_sync_$(date +%Y-%m-%d).log`
3. Test manuell sync: `python3 scripts/automated_protonord_sync.py`

### Kontakt
- **Teknisk**: Se logs og feilmeldinger
- **Konfigurasjon**: Rediger `config/sync_config.ini`

---

🎉 **ProtoNord Cloud Synkronisering er nå fullt automatisert!**

*Sist oppdatert: 2025-09-13*