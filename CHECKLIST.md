# 📋 Implementerings-sjekkliste

Bruk denne sjekklisten for å sette opp systemet steg for steg.

## ✅ Forberedelser (5-10 minutter)

### 1. Server/miljø-krav
- [ ] Linux-server med sudo-tilgang
- [ ] Python 3.12+ installert
- [ ] Git konfigurert med SSH-nøkler til GitHub
- [ ] Minst 10GB ledig diskplass

### 2. Shopify-tilganger
- [ ] Shopify-butikk med Admin-tilgang
- [ ] Custom App opprettet i Shopify Admin
- [ ] Admin API access token generert
- [ ] API-tilganger konfigurert:
  - [ ] `read_products`
  - [ ] `write_products`
  - [ ] `read_files`
  - [ ] `write_files`

## 🔧 Installasjons-trinn (10-15 minutter)

### 3. Klon og sett opp prosjekt
```bash
git clone https://github.com/PROTONORD/prototype-workflow-med-github.git
cd prototype-workflow-med-github
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
- [ ] Prosjekt klonet
- [ ] Virtuelt miljø opprettet
- [ ] Dependencies installert

### 4. MinIO-oppsett
```bash
sudo ./setup/install_minio.sh
```
- [ ] MinIO installert og startet
- [ ] Web-konsoll tilgjengelig på http://localhost:9001
- [ ] Standard-credentials endret (minioadmin/minioadmin123 → dine credentials)
- [ ] "products" bucket opprettet

### 5. Miljøkonfigurasjon
```bash
cp .env.example .env
nano .env  # Rediger med dine verdier
```
- [ ] `.env` fil opprettet og konfigurert med:
  - [ ] `SHOPIFY_SHOP=yourstore.myshopify.com`
  - [ ] `SHOPIFY_ACCESS_TOKEN=shpat_xxxxx`
  - [ ] `MINIO_ACCESS_KEY=din-access-key`
  - [ ] `MINIO_SECRET_KEY=din-secret-key`
  - [ ] `MINIO_BUCKET=products`

## 🧪 Testing og validering (5 minutter)

### 6. Test konfigurasjonen
```bash
python setup/validate_config.py
python setup/test_shopify_connection.py
```
- [ ] Alle konfigurasjonstester passert
- [ ] Shopify API-tilkobling verifisert
- [ ] MinIO-tilkobling verifisert

## 🚀 Første import (5-30 minutter, avhengig av antall produkter)

### 7. Import eksisterende produkter
```bash
python main.py bootstrap
```
- [ ] Alle produkter importert fra Shopify
- [ ] Lokale mapper opprettet i `catalog/`
- [ ] Produktbilder lastet opp til MinIO
- [ ] `catalog_summary.json` opprettet

### 8. Verifiser resultatet
```bash
python main.py status
ls catalog/  # Se alle produktmapper
```
- [ ] Katalog-status viser riktig antall produkter
- [ ] Produktmapper inneholder `product.json`, `description.md`, `README.md`

### 9. Første Git commit
```bash
git add catalog/
git commit -m "📦 Initial product catalog from Shopify"
git push
```
- [ ] Katalog committed til GitHub
- [ ] Endringer synlige på GitHub-repository

## 🔄 Test synkronisering (5 minutter)

### 10. Test sync tilbake til Shopify
```bash
# Dry run først (ingen endringer)
python main.py sync --dry-run

# Faktisk sync (valgfritt hvis dry run ser bra ut)
python main.py sync
```
- [ ] Dry run kjørt uten feil
- [ ] Faktisk sync testet (valgfritt)

## 🎯 Produksjons-setup (10-20 minutter)

### 11. Webhook-server (valgfritt for sanntidsoppdateringer)
```bash
pip install -r requirements-dev.txt
python setup/webhook_server.py --port 8080
```
- [ ] Webhook-server startet
- [ ] Shopify webhooks konfigurert (se IMPLEMENTATION.md)

### 12. GitHub Actions (valgfritt for automatisering)
- [ ] GitHub Secrets konfigurert med miljøvariabler
- [ ] Workflow-fil `.github/workflows/sync-products.yml` aktivert
- [ ] Test av manuell workflow-trigger

### 13. Cron job for automatisk sync (valgfritt)
```bash
crontab -e
# Legg til: 0 8 * * * cd /path/to/project && source .venv/bin/activate && python main.py sync
```
- [ ] Cron job konfigurert for daglig sync

## ✅ Ferdig! Neste steg

Når alle punkt over er sjekket av, er systemet klart for bruk:

### Daglig bruk:
1. **Opprett nytt produkt**: `python main.py new "Produktnavn" --type "Kategori"`
2. **Rediger produkter**: Endre `product.json` eller `description.md` i produktmapper
3. **Sync til Shopify**: `python main.py sync` eller `python main.py sync produkt-handle`
4. **Vis status**: `python main.py status`

### Upload filer til MinIO:
1. Åpne MinIO web-konsoll: http://localhost:9001
2. Naviger til `products/produkt-handle/`
3. Last opp filer til `images/`, `cad/`, eller `documentation/`

### GitHub samarbeid:
1. Opprett Issues for nye produktideer
2. Bruk Pull Requests for store endringer
3. Diskuter produktutvikling i kommentarer

---

## 🆘 Hvis noe går galt

### Vanlige problemer:
1. **MinIO starter ikke**: Sjekk `sudo journalctl -u minio -f`
2. **Shopify API-feil**: Verifiser access token og tilganger
3. **Python-import-feil**: Sjekk at virtual environment er aktivert
4. **Fil-tilgangsfeil**: Sjekk file permissions på data-kataloger

### Get help:
- Se `IMPLEMENTATION.md` for detaljerte instruksjoner
- Opprett GitHub Issue hvis du finner bugs
- Sjekk logs i `logs/` katalogen