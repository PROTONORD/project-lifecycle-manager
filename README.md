# prototype-workflow-med-github

### \#\# Hva som mangler

  * **Systemarkitektur:** En kort oversikt som forklarer den toveis dataflyten.
  * **Shopify API-oppsett:** Hvilke nøkler man trenger.
  * **Arbeidsflyten i praksis:**
      * Steg for éngangsimporten fra Shopify til GitHub.
      * Steg for den daglige bruken med å publisere fra GitHub til Shopify.

-----

### \#\# Her er den komplette og oppdaterte `README.md`-filen

Dette er versjonen som inkluderer **alt**, slik at den blir en komplett A-til-Å guide. Du kan erstatte den du har nå med denne.

# \#\# Komplett Guide for Automatisert CAD til E-handel

Dette dokumentet beskriver A-til-Å-oppsettet for et helautomatisert system som håndterer CAD-design fra idé til publisert produkt i en Shopify-butikk. Systemet er bygget rundt en sentral server, der **GitHub** fungerer som den definitive sannhetskilden (*Single Source of Truth*) for all produktinformasjon og designhistorikk.

-----

### \#\# Innholdsfortegnelse

1.  **Systemarkitektur: En oversikt**
2.  **Del 1: Grunnoppsett av Server**
      * 1.1. Installasjon av programvare
      * 1.2. Oppsett av nettverksdeling (Samba)
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

Systemet er designet for å være robust og skalerbart. All logikk og lagring skjer på en sentral Linux-server, noe som gjør det enkelt å jobbe fra hvilken som helst maskin (Windows, macOS, etc.).

  * **Kjerne:** En Linux-server som kjører alle automatiseringsskript og lagrer CAD-filene.
  * **Fildeling:** Samba deler prosjektmappene sikkert over det private nettverket.
  * **Nettverk:** Tailscale skaper et sikkert, privat nettverk mellom server og alle dine enheter, uansett hvor de er.
  * **Versjonskontroll:** Git sporer endringer, men `.gitignore` sørger for at kun en tekstbasert logg (`fil-logg.md`) lastes opp til GitHub, ikke de tunge CAD-filene.
  * **Integrasjon:** Python-skript bruker Shopify- og GitHub-APIene til å synkronisere produktdata begge veier.

-----

### \#\# 2. Del 1: Grunnoppsett av Server 🐧

#### **2.1. Installasjon av Programvare**

Koble til serveren (anbefalt: Ubuntu Server 22.04 LTS) og kjør følgende:

```bash
# Oppdater systemet og installer nødvendige pakker
sudo apt update && sudo apt upgrade -y
sudo apt install samba git python3 python3-pip

# Installer Python-biblioteker for API-kommunikasjon
pip3 install watchdog ShopifyAPI PyGithub
```

#### **2.2. Oppsett av Nettverksdeling (Samba)**

1.  **Opprett hovedmappe:**
    ```bash
    sudo mkdir -p /srv/cad-projects
    # Erstatt 'ditt-brukernavn' med ditt faktiske brukernavn på serveren
    sudo chown -R ditt-brukernavn:ditt-brukernavn /srv/cad-projects
    ```
2.  **Konfigurer Samba:** Rediger `sudo nano /etc/samba/smb.conf` og legg til på bunnen:
    ```ini
    [CAD-Projects]
    comment = Sentral lagring for alle CAD-prosjekter
    path = /srv/cad-projects
    read only = no
    browseable = yes
    valid users = ditt-brukernavn
    ```
3.  **Sett Samba-passord:** `sudo smbpasswd -a ditt-brukernavn` (dette blir nettverkspassordet).
4.  **Start tjenesten på nytt:** `sudo systemctl restart smbd`.

#### **2.3. Sikker Tilgang (Tailscale)**

1.  **Installer Tailscale** på serveren og alle dine klientmaskiner.
2.  **Start og autentiser:** Kjør `sudo tailscale up` på serveren og logg inn på alle enheter med samme konto.
3.  **Finn IP-adressen** til serveren i Tailscale-panelet. Den vil alltid starte med `100.x.x.x`.

-----

### \#\# 3. Del 2: Konfigurasjon av Versjonskontroll 🔄

#### **3.1. Git & SSH-oppsett**

For at serveren skal kunne kommunisere med GitHub uten passord, må en SSH-nøkkel settes opp.

1.  På serveren, generer en nøkkel: `ssh-keygen -t ed25519 -C "din-epost@eksempel.com"`.
2.  Kopier innholdet av `~/.ssh/id_ed25519.pub`.
3.  På GitHub, gå til **Settings \> SSH and GPG keys** og lim inn nøkkelen.

#### **3.2. Automatisering av Fillogg (`watcher.py`)**

Dette skriptet overvåker prosjektmappene og oppdaterer en `fil-logg.md` for hvert prosjekt som lastes opp til GitHub.

1.  **Plasser skriptet:** Legg `watcher.py`-skriptet i `/usr/local/bin/`.
2.  **Kjør i bakgrunnen:** Sett opp `github-watcher.service`-filen for å la `systemd` styre skriptet, slik at det alltid kjører.
    ```bash
    # Aktiver og start tjenesten
    sudo systemctl daemon-reload
    sudo systemctl enable github-watcher.service
    sudo systemctl start github-watcher.service
    ```

-----

### \#\# 4. Del 3: Shopify-integrasjon 🛒

#### **4.1. API-tilganger**

Du trenger to sett med nøkler:

  * **Shopify:** Opprett en "Privat App" i Shopify-adminpanelet for å få en **API-nøkkel** og et **API-passord**.
  * **GitHub:** Opprett et **Personal Access Token (PAT)** under **Settings \> Developer settings** på GitHub. Gi det `repo`-tilgang.

#### **4.2. Skriptene: Import og Publiser**

To hovedskript styrer dataflyten. Plasser begge i `/usr/local/bin/` på serveren.

  * `importer_fra_shopify.py`: Leser butikken din og oppretter den grunnleggende mappestrukturen for eksisterende produkter.
  * `publiser_til_shopify.py`: Leser en lokal prosjektmappe og oppretter/oppdaterer produktet i Shopify.

-----

### \#\# 5. Del 4: Arbeidsflyt i Praksis ⚙️

#### **5.1. Éngangsimport: Få oversikt over gamle design**

Dette gjøres kun én gang for å bygge arkivet ditt.

1.  **Koble til serveren:** `ssh ditt-brukernavn@SERVERENS_TAILSCALE_IP`.
2.  **Kjør importskriptet:** `python3 /usr/local/bin/importer_fra_shopify.py`.
3.  Vent mens skriptet oppretter mapper og repositorier for alle dine tidligere design.

#### **5.2. Daglig bruk: Fra nytt design til publisert produkt**

Dette er din standard arbeidsflyt for nye produkter.

1.  **Koble til nettverksstasjonen** fra din PC eller Mac.
2.  **Opprett prosjektmappen** (f.eks., `volvo-xc40-ladekabelholder`).
3.  **Sett opp Git:** Klon et nytt, tomt GitHub-repositorium inn i mappen.
4.  **Legg til standardfiler:**
      * En `.gitignore`-fil som ekskluderer CAD-filer og bilder.
      * En `product.json`-fil for Shopify-data.
5.  **Design og fyll mappen:** Legg til CAD-filer, bilder for butikken (`/images/shopify/`), og fyll ut all info i `product.json`.
6.  **Publiser:**
      * Koble til serveren via SSH.
      * Kjør publiseringsskriptet:
        ```bash
        python3 /usr/local/bin/publiser_til_shopify.py /srv/cad-projects/volvo-xc40-ladekabelholder
        ```
7.  **Ferdig\!** Produktet er nå i Shopify, og `watcher.py` vil fortsette å loggføre alle filendringer til GitHub.

-----

### \#\# 6. Del 5: Fremtidsplaner og Utvidelser 🚀

Dette systemet er en plattform for videre automatisering.

  * **Webhooks:** Bytt ut det manuelle publiseringsskriptet med et webhook fra GitHub for ekte sanntidspublisering.
  * **Fusion 360 API:** Utvikle et Add-in for å automatisere eksport og utfylling av data direkte fra CAD-programmet.
  * **Lagerstyring:** Utvid skriptene til å kunne oppdatere lagerstatus i Shopify basert på antall produserte enheter loggført i Git.
