# prototype-workflow-med-github

# \#\# Oppsett for Automatisert CAD Versjonskontroll

Dette repositoriet inneholder alt du trenger for å sette opp en sentralisert server som automatisk versjonskontrollerer CAD-prosjekter. Løsningen bruker en Linux-server, Samba for fildeling, og et Python-skript for å synkronisere en fillogg med et privat GitHub-repositorium. All nettverkstrafikk sikres via Tailscale. 💻

Målet er å ha en "lagre og glem"-løsning, der CAD-filer lagres lokalt på serveren, mens en lettvekts logg over alle endringer blir lastet opp til GitHub.

-----

### \#\# Innholdsfortegnelse

1.  **Serveroppsett**
      * Installasjon av programvare
      * Oppsett av Samba (fildeling)
      * Konfigurering av Git
2.  **Automatiseringsskript**
      * Konfigurering av `watcher.py`
      * Sette opp `systemd`-tjeneste
3.  **Prosjektkonfigurasjon**
      * Struktur for prosjektmapper
      * Bruk av `.gitignore`
4.  **Klientoppsett (Tailscale)**
      * Koble til fra Windows
      * Koble til fra macOS
5.  **Fremtidige forbedringer**
      * API-integrasjoner mot Fusion 360

-----

### \#\# 1. Serveroppsett 🐧

Disse stegene utføres på din dedikerte Linux-server (anbefalt: Ubuntu Server 22.04 LTS).

#### **Installasjon av Nødvendig Programvare**

Først, installer alle pakkene vi trenger.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install samba git python3 python3-pip
pip3 install watchdog
```

#### **Oppsett av Samba (Fildeling)**

Vi bruker Samba for å gjøre prosjektmappene tilgjengelige over nettverket.

1.  Opprett mappen som skal huse alle CAD-prosjektene.
    ```bash
    sudo mkdir -p /srv/cad-projects
    sudo chown -R din-bruker:din-bruker /srv/cad-projects
    ```
2.  Rediger Samba-konfigurasjonsfilen: `sudo nano /etc/samba/smb.conf`.
3.  Legg til følgende på bunnen av filen for å dele hovedmappen.
    ```ini
    [CAD-Projects]
    comment = Sentral lagring for alle CAD-prosjekter
    path = /srv/cad-projects
    read only = no
    browseable = yes
    guest ok = no
    valid users = din-bruker
    ```
4.  Sett et dedikert passord for Samba-tilgang (dette er **ikke** ditt vanlige Linux-passord).
    ```bash
    sudo smbpasswd -a din-bruker
    ```
5.  Start Samba på nytt for at endringene skal tre i kraft.
    ```bash
    sudo systemctl restart smbd
    ```

#### **Konfigurering av Git**

For at serveren skal kunne kommunisere med GitHub, anbefales det å sette opp en SSH-nøkkel.

1.  Generer en ny SSH-nøkkel på serveren.
2.  Legg til den offentlige nøkkelen (`~/.ssh/id_ed25519.pub`) under **Settings \> SSH and GPG keys** på din GitHub-konto.

-----

### \#\# 2. Automatiseringsskript 🤖

Skriptet `watcher.py` overvåker mappene og trigger synkronisering til GitHub.

#### **Konfigurering av `watcher.py`**

1.  Kopier `watcher-script/watcher.py` fra dette repositoriet til `/usr/local/bin/` på serveren din.
2.  Åpne skriptet og sørg for at `WATCH_PATH` peker til riktig mappe: `WATCH_PATH = r"/srv/cad-projects"`.

#### **Sette opp `systemd`-tjeneste**

For at skriptet skal kjøre kontinuerlig i bakgrunnen, setter vi det opp som en systemtjeneste.

1.  Kopier `server-setup/github-watcher.service.example` til `/etc/systemd/system/github-watcher.service`.
2.  Rediger filen og pass på at `User` og `ExecStart`-stiene er korrekte.
3.  Aktiver og start tjenesten.
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable github-watcher.service
    sudo systemctl start github-watcher.service
    ```
    Du kan sjekke statusen med `sudo systemctl status github-watcher.service`.

-----

### \#\# 3. Prosjektkonfigurasjon 📂

Hvert nye CAD-prosjekt trenger en spesifikk struktur og en `.gitignore`-fil.

#### **Struktur for Prosjektmapper**

Når du starter et nytt prosjekt, f.eks. "Ford Mustang Deksel", opprett en ny mappe i `/srv/cad-projects/` og klon det tilhørende GitHub-repositoriet inn i den. Anbefalt struktur inne i prosjektmappen er:

  * `/cad/` - For .f3d, .step etc.
  * `/production/` - For .stl, .3mf og G-kode.
  * `/docs/` - For bilder og testresultater.

#### **Bruk av `.gitignore`**

Dette er den viktigste filen for å unngå opplasting av store filer. I roten av **hvert** prosjekt-repositorium, opprett en fil kalt `.gitignore` med følgende innhold:

```
# Ignorer alle CAD, CAM og store filer
*.f3d
*.f3z
*.stl
*.step
*.obj
*.3mf
*.gcode

# Ignorer bilder og videoer
*.png
*.jpg
*.jpeg
*.mov
*.mp4

# Ignorer systemfiler
.DS_Store
Thumbs.db
```

**Kun `fil-logg.md` og `.gitignore` vil bli lastet opp til GitHub.**

-----

### \#\# 4. Klientoppsett (Tailscale) 🌐

For sikker og enkel tilgang fra alle enheter, installer [Tailscale](https://tailscale.com/) på serveren og alle klientmaskiner (PC, Mac, laptop).

1.  Installer Tailscale på serveren og kjør `sudo tailscale up`.
2.  Installer Tailscale på dine klienter og logg inn med samme konto.
3.  Finn serverens Tailscale IP-adresse (alltid `100.x.x.x`) i Tailscale-adminpanelet.

#### **Koble til fra Windows**

  * **Filutforsker \> Høyreklikk "Denne PCen" \> Koble til en nettverksstasjon...**
  * **Mappe:** `\\SERVERENS_TAILSCALE_IP\CAD-Projects`
  * Logg inn med ditt Samba-brukernavn og -passord.

#### **Koble til fra macOS**

  * **Finder \> Gå \> Koble til tjener...** (Cmd+K)
  * **Tjeneradresse:** `smb://SERVERENS_TAILSCALE_IP/CAD-Projects`
  * Logg inn med ditt Samba-brukernavn og -passord.

-----

### \#\# 5. Fremtidige Forbedringer 🚀

Dette systemet er designet for å være utvidbart.

#### **API-integrasjoner mot Fusion 360**

Fusion 360 har et API som kan brukes til å automatisere prosesser. Fremtidige forbedringer kan inkludere:

  * Et Fusion 360 Add-in som automatisk eksporterer `.stl` og `.step` til riktig mappe på serveren ved lagring.
  * Et skript som henter produksjonstid og materialbruk fra Fusion 360 og legger det til i `fil-logg.md`.

Alle nye skript eller integrasjoner vil bli lagt til og dokumentert i dette repositoriet.
