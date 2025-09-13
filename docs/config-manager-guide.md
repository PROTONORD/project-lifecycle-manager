# CONFIG MANAGER - Universalt Konfigurasjonsverktøy

## 🎯 Formål

`config_manager.sh` er et universalt verktøy for å administrere konfigurasjonsfiler på en trygg og konsistent måte. Det erstatter manuelle redigeringer av kritiske filer som crontab, YAML, hosts, osv.

## 🚀 Funksjoner

### Automatisk backup
- Lager sikkerhetskopi før alle endringer
- Timestamp-baserte backup-filer
- Enkel gjenoppretting fra backup

### Støttede konfigurasjonstyper
- **crontab** - Cron-jobber
- **yaml** - YAML-filer
- **json** - JSON-filer (begrenset støtte)
- **conf** - Generelle konfigurasjonsfiler
- **env** - Environment-filer
- **hosts** - /etc/hosts
- **nginx** - Nginx-konfigurasjon
- **apache** - Apache-konfigurasjon

### Sikre operasjoner
- Dry run-modus for testing
- Duplikatsjekk for crontab
- Verbose logging
- Feilhåndtering

## 📖 Brukseksempler

### Crontab-administrasjon

```bash
# Legg til ny cron-jobb med backup
./scripts/config_manager.sh -b add crontab "30 1 * * * /path/to/script.sh"

# Vis nåværende crontab
./scripts/config_manager.sh show crontab

# Fjern cron-jobb
./scripts/config_manager.sh remove crontab "30 1 * * * /path/to/script.sh"

# Lag backup av crontab
./scripts/config_manager.sh backup crontab

# Gjenopprett fra backup
./scripts/config_manager.sh restore crontab crontab_20250913_141431.backup
```

### YAML-filer

```bash
# Legg til YAML-innhold
./scripts/config_manager.sh -f config.yml add yaml "database: production"

# Vis YAML-fil
./scripts/config_manager.sh -f config.yml show yaml

# Test endring (dry run)
./scripts/config_manager.sh -f config.yml -d add yaml "new_setting: value"
```

### Hosts-fil

```bash
# Legg til hosts-oppføring
./scripts/config_manager.sh add hosts "127.0.0.1 mysite.local"

# Fjern hosts-oppføring
./scripts/config_manager.sh remove hosts "mysite.local"
```

## 🛠 Kommandostruktur

```
config_manager.sh [OPSJONER] ACTION CONFIG_TYPE [CONTENT]
```

### Actions
- `add` - Legg til innhold
- `remove` - Fjern innhold  
- `backup` - Lag backup
- `restore` - Gjenopprett fra backup
- `show` - Vis konfigurasjon

### Opsjoner
- `-f FILE` - Spesifiser fil (for yaml, json, conf)
- `-b` - Lag backup før endring
- `-v` - Verbose output
- `-d` - Dry run (test-modus)
- `-h` - Vis hjelp

## 📁 Backup-system

### Automatisk organisering
```
~/.config_backups/
├── crontab_20250913_141431.backup
├── hosts_20250913_142500.backup
└── config.yml_20250913_143000.backup
```

### Backup-strategier
- **Automatisk**: Bruk `-b` flagget
- **Manuell**: `backup` action
- **Timestamp**: Alle backuper har unike navn
- **Sikker gjenoppretting**: Validering før restore

## 🔒 Sikkerhetsfunksjoner

### Duplikatsjekk
```bash
# Forhindrer duplikate cron-oppføringer
./scripts/config_manager.sh add crontab "0 2 * * * script.sh"
# [WARNING] Cron-oppføring eksisterer allerede
```

### Dry run testing
```bash
# Test før faktisk endring
./scripts/config_manager.sh -d add crontab "test entry"
# [INFO] DRY RUN: Ville lagt til 'test entry' i crontab
```

### Automatisk logging
- Alle operasjoner logges til `~/config_manager.log`
- Timestamp og handling registreres
- Feil og advarsler dokumenteres

## 🎨 Brukstilfeller i ProtoNord

### 1. Cron-jobber
```bash
# ProtoNord backup (allerede implementert)
./scripts/config_manager.sh -b add crontab "30 1 * * * /home/kau005/prototype-workflow-med-github/scripts/protonord_cloud_backup.sh >> /home/kau005/protonord_backup.log 2>&1"

# Shopify sync-jobb
./scripts/config_manager.sh -b add crontab "0 */6 * * * /home/kau005/prototype-workflow-med-github/scripts/shopify_sync.sh"
```

### 2. Docusaurus konfigurasjon
```bash
# Legg til nye innstillinger
./scripts/config_manager.sh -f docusaurus.config.js -b add conf "  customField: 'value',"
```

### 3. Environment variabler
```bash
# API-nøkler og konfigurasjon
./scripts/config_manager.sh -f .env -b add env "BACKUP_ENABLED=true"
```

## 🔧 Avansert bruk

### Batch-operasjoner
```bash
# Flere cron-jobber samtidig
for job in "0 1 * * * script1.sh" "0 2 * * * script2.sh"; do
    ./scripts/config_manager.sh -b add crontab "$job"
done
```

### Betinget tillegg
```bash
# Legg til kun hvis ikke eksisterer
if ! ./scripts/config_manager.sh show crontab | grep -q "my_script"; then
    ./scripts/config_manager.sh -b add crontab "0 3 * * * my_script.sh"
fi
```

### Backup-rotasjon
```bash
# Automatisk cleanup av gamle backuper (kan legges i cron)
find ~/.config_backups -name "*.backup" -mtime +30 -delete
```

## 📊 Logging og overvåkning

### Sjekk operasjonslogg
```bash
# Vis siste operasjoner
tail -20 ~/config_manager.log

# Søk etter feil
grep "ERROR\|WARNING" ~/config_manager.log

# Spesifikk konfigurasjon
grep "crontab" ~/config_manager.log
```

### Status-rapporter
```bash
# Lag rapport over alle konfigurasjoner
./scripts/config_manager.sh show crontab > ~/config_status.txt
echo "=== HOSTS ===" >> ~/config_status.txt
./scripts/config_manager.sh show hosts >> ~/config_status.txt
```

## 🚨 Feilsøking

### Vanlige problemer

#### Tilgangsrettigheter
```bash
# Fiks executable-rettigheter
chmod +x /home/kau005/prototype-workflow-med-github/scripts/config_manager.sh
```

#### Backup-mappe
```bash
# Manuell opprettelse hvis nødvendig
mkdir -p ~/.config_backups
```

#### Crontab-problemer
```bash
# Valider cron-syntax
./scripts/config_manager.sh -d add crontab "invalid syntax"
```

## 📈 Fremtidige utvidelser

### Planlagte funksjoner
- [ ] JSON-parsing med `jq`
- [ ] Nginx/Apache konfigurasjonsvalidering
- [ ] Git-integrert backup
- [ ] Web-interface for administrasjon
- [ ] Automatisk konfigurasjon-sync mellom servere

Dette verktøyet er nå standard for alle konfigurasjonshåndteringer i ProtoNord-miljøet!