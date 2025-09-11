# prototype-workflow-med-github

# \#\# Komplett Guide for Automatisert CAD til E-handel med MinIO

Dette dokumentet beskriver A-til-Å-oppsettet for et helautomatisert system som håndterer CAD-design fra idé til publisert produkt i en Shopify-butikk. Systemet er bygget rundt en sentral server som bruker **MinIO** for robust fillagring, og **GitHub** som den definitive sannhetskilden (*Single Source of Truth*) for all produktinformasjon og designhistorikk.

-----

### \#\# Innholdsfortegnelse

1.  **Systemarkitektur: En oversikt**
2.  **Del 1: Grunnoppsett av Server**
      * 1.1. Installasjon av programvare
      * 1.2. Oppsett av MinIO (Objektlagring)
      * 1.3. Sikker tilgang (Tailscale)
3.  **Del 2: Konfigurasjon av Versjonskontroll**
      * 2.1. Git & SSH-oppsett
      * 2.2. Automatisering av fillogg (`watcher.py`)
4.  **Del 3: Shopify-integrasjon**
      * 3.1. API-tilganger
      * 3.2. Skriptene: Import og Publiser
5.  **Del 4: Arbeidsflyt i Praksis**
      * 4.1. Éngangsimport: Få oversikt over gamle design
      * 4.2. Daglig bruk: Fra nytt design til publisert produkt
6.  **Del 5: Fremtidsplaner og Utvidelser**

-----

### \#\# 1. Systemarkitektur: En oversikt 🏗️

Systemet er designet for å være profesjonelt, sikkert og skalerbart.

  * **Kjerne:** En Linux-server som kjører alle automatiseringsskript.
  * **Lagring:** **MinIO** fungerer som en privat S3-skylagring for alle store filer (CAD, bilder etc.). Dette gir oss versjonering, datasikkerhet (erasure coding) og API-tilgang.
  * **Nettverk:** Tailscale skaper et sikkert, privat nettverk mellom server og alle dine enheter.
  * **Versjonskontroll:** Git sporer endringer. `.gitignore` sørger for at kun en tekstbasert logg (`fil-logg.md`) og konfigurasjonsfiler (`product.json`) lastes opp til GitHub.
  * **Integrasjon:** Python-skript bruker Shopify-, GitHub- og MinIO-APIene til å synkronisere data.

-----

### \#\# 2. Del 1: Grunnoppsett av Server 🐧

#### **2.1. Installasjon av Programvare**

Koble til serveren (anbefalt: Ubuntu Server 22.04 LTS) og kjør følgende:

```bash
# Oppdater systemet og installer nødvendige pakker
sudo apt update && sudo apt upgrade -y
sudo apt install git python3 python3-pip

# Installer Python-biblioteker for API-kommunikasjon
pip3 install watchdog ShopifyAPI PyGithub minio
```

#### **2.2. Oppsett av MinIO (Objektlagring)**

MinIO vil håndtere all lagring av store filer.

1.  **Installer MinIO:** Følg den offisielle guiden for å installere MinIO Server på Linux.
2.  **Start MinIO Server:** Start serveren, gjerne som en `systemd`-tjeneste for at den alltid skal kjøre. Noter deg tilgangsnøkkel (`access key`) og hemmelig nøkkel (`secret key`).
3.  **Opprett en "Bucket":** Logg inn på MinIO sitt web-grensesnitt (vanligvis `http://DIN_SERVER_IP:9000`). Opprett en ny "bucket" kalt `cad-projects`.
4.  **Aktiver Versjonering (Anbefalt):** I innstillingene for `cad-projects`-bøtten, slå på versjonering. Dette beskytter mot utilsiktet overskriving av filer.

#### **2.3. Sikker Tilgang (Tailscale)**

1.  **Installer Tailscale** på serveren og alle dine klientmaskiner.
2.  **Start og autentiser:** Kjør `sudo tailscale up` på serveren og logg inn på alle enheter med samme konto.
3.  **Finn IP-adressen** til serveren i Tailscale-panelet.

-----

### \#\# 3. Del 2: Konfigurasjon av Versjonskontroll 🔄

#### **3.1. Git & SSH-oppsett**

Sett opp en SSH-nøkkel mellom serveren og GitHub for passordfri kommunikasjon.

1.  På serveren, generer en nøkkel: `ssh-keygen -t ed25519`.
2.  På GitHub, gå til **Settings \> SSH and GPG keys** og lim inn den offentlige nøkkelen.

#### **3.2. Automatisering av Fillogg (`watcher.py`)**

Dette skriptet lytter etter hendelser i MinIO og oppdaterer `fil-logg.md` i det relevante GitHub-repoet.

1.  **Konfigurer Webhook:** I MinIO, sett opp en webhook for `cad-projects`-bøtten som sender en varsling til en liten webtjeneste på serveren din hver gang en fil lastes opp eller slettes.
2.  **Oppdater `watcher.py`:** Skriptet må endres fra å overvåke et filsystem til å motta disse webhook-varslingene. Når det mottar en varsling, henter det fil-metadata fra MinIO og oppdaterer og pusher `fil-logg.md` til GitHub.
3.  **Kjør i bakgrunnen:** Sett opp `watcher.py` som en `systemd`-tjeneste.

-----

### \#\# 4. Del 3: Shopify-integrasjon 🛒

#### **4.1. API-tilganger**

  * **Shopify:** Opprett en "Privat App" for å få **API-nøkkel** og **passord**.
  * **GitHub:** Opprett et **Personal Access Token (PAT)** med `repo`-tilgang.
  * **MinIO:** Bruk **Access Key** og **Secret Key** fra da du startet MinIO-serveren.

#### **4.2. Skriptene: Import og Publiser**

Skriptene må oppdateres til å bruke MinIO.

  * `importer_fra_shopify.py`: Oppretter mapper lokalt for Git, men oppretter også en tilsvarende "mappe"-struktur i MinIO-bøtten.
  * `publiser_til_shopify.py`: Leser `product.json`, henter produktbilder fra MinIO, og publiserer til Shopify.

-----

### \#\# 5. Del 4: Arbeidsflyt i Praksis ⚙️

#### **5.1. Éngangsimport: Få oversikt over gamle design**

1.  **Kjør importskriptet:** `python3 /usr/local/bin/importer_fra_shopify.py`.
2.  Skriptet oppretter GitHub-repositorier og MinIO-mapper for eksisterende produkter.

#### **5.2. Daglig bruk: Fra nytt design til publisert produkt**

1.  **Opprett Git-prosjekt:** Lag et nytt, tomt GitHub-repositorium. Klon det til en midlertidig mappe lokalt.
2.  **Legg til standardfiler:** Legg til `.gitignore` og en `product.json`. Fyll ut `product.json`.
3.  **Last opp filer til MinIO:** Bruk en S3-klient (som Cyberduck) eller MinIO sitt web-grensesnitt for å koble til serveren din over Tailscale. Opprett en ny "mappe" i `cad-projects`-bøtten og last opp dine CAD-filer, bilder, etc.
4.  **Push til GitHub:** Push `product.json` og `.gitignore` til GitHub.
5.  **Publiser til Shopify:**
      * Koble til serveren via SSH.
      * Kjør publiseringsskriptet: `python3 /usr/local/bin/publiser_til_shopify.py --project-name volvo-xc40-ladekabelholder`.
6.  **Ferdig\!** Produktet er i Shopify. `watcher.py` har allerede registrert filene du lastet opp til MinIO og oppdatert `fil-logg.md` på GitHub.

-----

### \#\# 6. Del 5: Fremtidsplaner og Utvidelser 🚀

  * **Fusion 360 Add-in:** Utvikle et Add-in som kan laste opp filer direkte til MinIO og oppdatere `product.json`.
  * **Sikker fildeling:** Bruk MinIO til å generere midlertidige nedlastingslenker for betatestere.
  * **Lagerstyring:** Utvid skriptene til å kunne oppdatere lagerstatus i Shopify.

## Del 7: Arkivering til Kunnskapsbase (Docmost) 📚
Når et produkt er ferdigstilt, testet og ansett som "modent", blir den endelige dokumentasjonen overført fra det aktive GitHub-prosjektet til vår sentrale, søkbare kunnskapsbase i Docmost.

Dette sikrer at vi bygger et permanent bibliotek over alle våre design, tilgjengelig for hele teamet, uavhengig av det aktive utviklingsløpet.

Hvorfor Docmost?
GitHub er vårt levende "verksted" for pågående utvikling, testing og samarbeid.

Docmost er vårt ferdige "bibliotek" for publisert, versjonert og lett søkbar informasjon.

Prosessen for overføring:
Når et prosjekt skal arkiveres, følges disse stegene:

Samle Dokumentasjon: All relevant informasjon fra prosjektets GitHub-repositorium – som hoved-README.md, monteringsguider, testresultater og designvalg – blir samlet.

Opprett Struktur i Docmost: Et nytt "Space" eller en ny "Book" opprettes i Docmost for produktet.

Lim inn Markdown: Innholdet fra .md-filene kopieres og limes direkte inn i Docmost-editoren. Plattformen formaterer teksten automatisk.

Last opp Filer: Relevante bilder, PDF-er og andre endelige filer lastes opp direkte til Docmost-siden for å sikre at all informasjon er samlet på ett sted.

Lenk Tilbake: En lenke til det opprinnelige GitHub-repositoriet legges ved i Docmost for de som trenger tilgang til den komplette, detaljerte endringshistorikken.


Ja, det er en veldig god idé. En kildeliste gjør prosjektdokumentasjonen din mye mer profesjonell og nyttig, både for deg selv og for andre som ser på den. Det viser hvilke byggeklosser systemet består av.

Her er et forslag til en komplett kildeseksjon som du kan lime rett inn i `README.md`-filen din. Den inkluderer Shopify-APIet og alle de andre sentrale teknologiene vi har diskutert.

-----

**(Lim inn dette i `prototype-workflow-med-github/README.md`)**

-----

### \#\# Kilder og Nyttige Ressurser 📚

Denne seksjonen inneholder lenker til den offisielle dokumentasjonen og hovedsidene for de sentrale teknologiene og tjenestene som brukes i dette prosjektet.

#### Plattformer og Kjernekomponenter

  * **[Git](https://git-scm.com/)** - Det distribuerte versjonskontrollsystemet som ligger i bunn for alt.
  * **[GitHub](https://docs.github.com/)** - Plattformen for kodelagring, samarbeid og automatisering.
  * **[Python](https://www.python.org/)** - Hovedspråket som brukes for alle automatiseringsskript.
  * **[MinIO](https://min.io/)** - Selv-hostet, S3-kompatibel objektlagring for alle store filer.
  * **[Tailscale](https://tailscale.com/)** - Verktøyet som bygger det sikre, private nettverket mellom enhetene.
  * **[Docmost](https://docmost.com/)** - Den selv-hostede kunnskapsbasen for endelig produktdokumentasjon.

#### API-er for Datautveksling

  * **[Shopify API](https://shopify.dev/docs/api)** - For programmatisk håndtering av produkter, kunder og ordre i nettbutikken.
  * **[Fiken API](https://www.google.com/search?q=https://fiken.no/api/dokumentasjon/)** - For automatisert opprettelse av kunder og fakturaer i regnskapssystemet.
  * **[Brønnøysundregistrene (Enhetsregisteret API)](https://data.brreg.no/enhetsregisteret/api/docs/index.html)** - For å hente og validere offisiell informasjon om norske foretak.
  * **[Stripe API](https://stripe.com/docs/api)** - For å håndtere betalinger og abonnenter.
  * **[NewsAPI.org](https://newsapi.org/)** - Et eksempel på en API for å hente nyhetsartikler for omdømmeanalyse.

#### Python-biblioteker (Et utvalg)

  * **[MinIO Python Client](https://min.io/docs/minio/linux/developers/python/API.html)** - For å kommunisere med MinIO-serveren.
  * **[PyGithub](https://pygithub.readthedocs.io/en/latest/)** - For å interagere med GitHub API.
  * **[ShopifyAPI for Python](https://github.com/Shopify/shopify_python_api)** - For å interagere med Shopify API.

#### Frontend- og Backend-rammeverk

  * **[FastAPI](https://fastapi.tiangolo.com/)** - Et moderne og raskt Python-rammeverk for å bygge backend-APIer.
  * **[Next.js](https://nextjs.org/)** - Et populært React-rammeverk for å bygge den klient-vendte nettbutikken.

