# ProtoNord Wiki - Prosjektstyring og Workflow-oversikt

Dette er en Docusaurus-basert wiki og prosjektstyringsplattform for ProtoNord som holder oversikt over hele arbeidsflyt fra idé til ferdig produkt. Systemet integrerer filserver-innhold med Shopify-produkter for å gi komplett sporbarhet og status på alle prosjekter.

## 🎯 Hovedfunksjoner

- **Prosjektoversikt**: Status på alle prosjekter (planlagt, under arbeid, ferdig)
- **Shopify-integrasjon**: Kobler produkter i butikk med designfiler og dokumentasjon
- **Filserver-kobling**: Oversikt over CAD-filer, bilder og dokumentasjon lagret i cloud
- **Workflow-sporing**: Fra første skisse til publisert produkt i Shopify
- **Dashboard**: Visuell oversikt over hele produksjonsløypa

## 🌐 Live nettsteder

- **Wiki og Dashboard**: <https://wiki.protonord.no>
- **Repository**: <https://github.com/PROTONORD/project-lifecycle-manager>

## 🏗️ Systemarkitektur

### Frontend (Docusaurus Wiki)

- **Port**: 3001 (lokal utvikling)
- **Framework**: Docusaurus v3 med React komponenter
- **Innhold**:
  - Prosjektdokumentasjon og workflow-status
  - Shopify-dashboard for produktoversikt
  - Filserver-integrasjon og cloud backup-dokumentasjon
  - Sporbarhet fra designfiler til ferdig produkt

### Prosjektstyring og Integrasjoner

- **Shopify API**: Dashboard som viser produkter som er publisert i butikk
- **Cloud Storage**: Google Drive + Jottacloud for designfiler og dokumentasjon
- **Filserver-kobling**: Oversikt over CAD-filer, bilder og prosjektfiler
- **Status-sporing**: Hvilke prosjekter som er planlagt, under arbeid eller ferdig
- **Backup System**: GFS strategi med dual-cloud redundans

### Infrastruktur

- **Web Server**: Apache med Let's Encrypt SSL
- **Automatisering**: Cron-baserte scripts
- **Versjonskontroll**: GitHub som single source of truth

## 🚀 Kom i gang

### 1. Installer dependencies

```bash
# Klon prosjektet
git clone https://github.com/PROTONORD/project-lifecycle-manager.git
cd project-lifecycle-manager

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
project-lifecycle-manager/
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

- **Prosjektstatus-dashboard**: Oversikt over hvilke prosjekter som er publisert som produkter
- **Produktkobling**: Kobler Shopify-produkter med tilhørende designfiler og dokumentasjon
- **Workflow-sporing**: Fra første CAD-fil til ferdig produkt i butikk
- **Lagerstatus**: Real-time oversikt over tilgjengelighet
- **API Integration**: Sikker tilgang til Shopify-data for prosjektstyring
- **Status-synkronisering**: Automatisk oppdatering av prosjektstatus basert på Shopify-data

### Cloud Backup System

- **GFS Strategi**: Grandfather-Father-Son backup rotasjon
- **Dual Cloud**: Google Drive + Jottacloud redundans
- **Automatisk cleanup**: Fjerner gamle backuper
- **Logging**: Detaljert backup-logg

## � Prosjekt Workflow

### Livssyklus: Fra Idé til Produkt

1. **Planlagt** 📋
   - Idé registreres i system
   - Designskisser og krav dokumenteres
   - Prosjektmappe opprettes i cloud storage

2. **Under arbeid** 🛠️
   - CAD-design og 3D-modellering
   - Prototyping og testing
   - Filer synkroniseres til filserver
   - Dokumentasjon oppdateres fortløpende

3. **Klar for produksjon** ✅
   - Design ferdigstilt og validert
   - Produktbilder og beskrivelser klare
   - Alle filer organisert i cloud storage

4. **Publisert i Shopify** 🛒
   - Produkt opprettet i Shopify-butikk
   - Kobling mellom filserver-filer og Shopify-produkt etablert
   - Status synkroniseres automatisk

### Filserver-integrasjon

- **CAD-filer**: `.step`, `.stl`, `.dwg` filer i organiserte mapper
- **Produktbilder**: Høyoppløselige bilder for web og print
- **Dokumentasjon**: README-filer med produktinformasjon
- **Status-sporing**: Automatisk deteksjon av prosjektstatus basert på filstruktur

## �🛠️ Utviklingsverktøy

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
