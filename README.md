# ProtoNord - Automatisert E-handel Platform

Dette er en helautomatisert e-handelsplattform som integrerer Shopify med cloud-basert fillagring og backup-systemer.

## 🌐 Live nettsteder

- **Hovedside**: <https://wiki.protonord.no>
- **Repository**: <https://github.com/PROTONORD/prototype-workflow-med-github>

## 🏗️ Systemarkitektur

### Frontend (Docusaurus)

- **Port**: 3001 (lokal utvikling)
- **Framework**: Docusaurus v3
- **Features**: Dark mode, React komponenter, Shopify dashboard

### Backend Integrasjoner

- **Shopify API**: Automatisk produktsynkronisering
- **Cloud Storage**: Google Drive + Jottacloud via rclone
- **Backup System**: GFS strategi med dual-cloud redundans

### Infrastruktur

- **Web Server**: Apache med Let's Encrypt SSL
- **Automatisering**: Cron-baserte scripts
- **Versjonskontroll**: GitHub som single source of truth

## 🚀 Kom i gang

### 1. Installer dependencies

```bash
# Klon prosjektet
git clone https://github.com/PROTONORD/prototype-workflow-med-github.git
cd prototype-workflow-med-github

# Installer Node.js pakker
npm install

# Installer Python dependencies
pip install -r requirements.txt
```

### 2. Konfigurer miljøvariabler

```bash
# Kopier mal og fyll inn verdier
cp .env.template .env
```

Påkrevde variabler:

```bash
# Shopify konfigurasjon
SHOPIFY_SHOP_URL=din-butikk.myshopify.com
SHOPIFY_ACCESS_TOKEN=din_access_token
SHOPIFY_API_KEY=din_api_key
SHOPIFY_API_SECRET=din_api_secret

# Data konfigurasjon
DATA_ROOT=catalog
```

### 3. Start utviklingsserver

```bash
# Start Docusaurus
npm start

# Eller i produksjon
npm run build
npm run serve
```

## 📁 Prosjektstruktur

```
prototype-workflow-med-github/
├── docs/                    # Dokumentasjon (Markdown)
│   ├── backup-system.md     # Backup system guide
│   └── config-manager-guide.md # Config manager manual
├── src/                     # React komponenter
│   ├── components/          # Gjenbrukbare komponenter
│   │   ├── ProtoNordHome.js # Hovedside komponent
│   │   └── ShopifyDashboard.js # Shopify dashboard
│   └── pages/               # Docusaurus sider
├── static/                  # Statiske filer
│   ├── data/shopify/        # Shopify JSON data
│   └── img/                 # Bilder og ikoner
├── scripts/                 # Automatiseringsscripts
│   ├── protonord_cloud_backup.sh    # Cloud backup system
│   ├── config_manager.sh            # Universal config manager
│   └── automated_protonord_sync.py  # Shopify sync script
├── catalog/                 # Produktkatalog
└── data/                    # Lokale datafiler
```

## 🔄 Automatisering

### Cron Schedule

```bash
# Daglig backup (01:30)
30 1 * * * /path/to/protonord_cloud_backup.sh

# Shopify sync (02:00)  
0 2 * * * /path/to/automated_protonord_sync.py

# Docker backup (søndager 03:00)
0 3 * * 0 /path/to/backup_docker.sh
```

### Shopify Integrasjon

- **Produktdata**: Automatisk sync fra Shopify API
- **Lagerinfo**: Real-time lagerstatus
- **Bestillinger**: Dashboard med ordre-oversikt
- **Synkronisering**: Daglig oppdatering via cron

### Cloud Backup System

- **GFS Strategi**: Grandfather-Father-Son backup rotasjon
- **Dual Cloud**: Google Drive + Jottacloud redundans
- **Automatisk cleanup**: Fjerner gamle backuper
- **Logging**: Detaljert backup-logg

## 🛠️ Utviklingsverktøy

### Config Manager

Universelt verktøy for konfigurasjonsadministrasjon:

```bash
# Legg til cron-jobb
./scripts/config_manager.sh -b add crontab "0 2 * * * script.sh"

# Administrer YAML/JSON filer
./scripts/config_manager.sh -f config.yml add yaml "setting: value"

# Backup og restore
./scripts/config_manager.sh backup crontab
./scripts/config_manager.sh restore crontab backup_file.backup
```

### Backup System

```bash
# Manuell backup
./scripts/protonord_cloud_backup.sh

# Sjekk backup-status  
tail -f ~/protonord_backup.log

# Test cloud-tilkobling
rclone lsd gdrive:
rclone lsd jottacloud:
```

## 🎨 Frontend Features

### Dark Mode Support

- Automatisk tema-deteksjon
- Responsivt design for alle skjermstørrelser
- Konsistent styling på tvers av komponenter

### Shopify Dashboard

- Real-time produktoversikt
- Lagerstatistikk og trender
- Bestillings-tracking
- Interaktive charts og grafer

### React Komponenter

- ProtoNordHome: Hovedside med produktkatalog
- ShopifyDashboard: Admin dashboard
- Responsive navigation og layout

## 🔐 Sikkerhet

### API Sikkerhet

- Environment variabler for sensitive data
- Rate limiting på API-kall
- Secure webhook endpoints

### Backup Sikkerhet

- Krypterte cloud-forbindelser
- Redundant lagring på multiple tjenester
- Automatisk integritetstesting

### Access Control

- GitHub-basert tilgangskontroll
- SSL/TLS for all web-trafikk
- Secure cron-job konfiguration

## 📊 Monitoring og Logging

### System Logs

```bash
# Backup logs
tail -f ~/protonord_backup.log

# Config manager logs
tail -f ~/config_manager.log

# Sync logs  
tail -f logs/cron.log
```

### Performance Monitoring

- Shopify API responstider
- Cloud upload statistikk
- Website laste-tider
- Error tracking og alerting

## 🚨 Feilsøking

### Vanlige problemer

#### Shopify API feil

```bash
# Test API tilkobling
curl -H "X-Shopify-Access-Token: $TOKEN" https://shop.myshopify.com/admin/api/2023-10/products.json
```

#### Cloud backup problemer

```bash
# Test rclone konfigurasjon
rclone config show
rclone lsd gdrive:
rclone lsd jottacloud:
```

#### Build/Deploy feil

```bash
# Clear cache og rebuild
npm run clear
npm install
npm run build
```

## 🔗 Relaterte Prosjekter

- **Tromsoskapere Wiki**: <https://wiki.tromsoskapere.no>
- **ProtoNord Shopify**: <https://protonord.myshopify.com>

## 📚 Dokumentasjon

### API Referanser

- [Shopify Admin API](https://shopify.dev/api/admin)
- [Docusaurus Documentation](https://docusaurus.io/)
- [rclone Documentation](https://rclone.org/)

### Interne Guider

- [Backup System Guide](docs/backup-system.md)
- [Config Manager Manual](docs/config-manager-guide.md)

## 🤝 Bidrag

1. Fork prosjektet
2. Opprett feature branch (`git checkout -b feature/ny-funksjon`)
3. Commit endringene (`git commit -m 'Legg til ny funksjon'`)
4. Push til branch (`git push origin feature/ny-funksjon`)
5. Opprett Pull Request

## 📝 Lisens

Dette prosjektet er proprietært for ProtoNord AS.

---

**Sist oppdatert**: September 2025  
**Versjon**: 2.0  
**Vedlikeholdt av**: ProtoNord Development Team
