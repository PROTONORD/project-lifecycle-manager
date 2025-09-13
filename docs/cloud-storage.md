---
sidebar_position: 2
---

# Cloud Storage Setup

Guide for å sette opp rclone med Jottacloud og Google Drive.

## Installasjon av rclone

```bash
curl https://rclone.org/install.sh | sudo bash
```

## Konfigurering

### Jottacloud

```bash
rclone config
# Velg "n" for new remote
# Navn: jottacloud
# Type: jottacloud
# Følg autentisering
```

### Google Drive

```bash
rclone config
# Velg "n" for new remote  
# Navn: gdrive
# Type: drive
# Følg autentisering
```

## Test tilkobling

```bash
# Test Jottacloud
rclone ls jottacloud:

# Test Google Drive
rclone ls gdrive:
```

## Neste steg

Når rclone er konfigurert, kan du:
1. Synkronisere filer automatisk
2. Generere filkatalog
3. Sette opp webhooks for automatisk oppdatering