#!/bin/bash

# =================================================================
# PROTONORD WEBSITE BACKUP TIL TO SKYTJENESTER (GOOGLE DRIVE + JOTTACLOUD)
# =================================================================

# --- INNSTILLINGER ---
# Definer begge Rclone-remotes
REMOTE_1_NAME="gdrive"
REMOTE_1_BASE_DIR="ProtoNordBackup"

REMOTE_2_NAME="jottacloud"
REMOTE_2_BASE_DIR="ProtoNordBackup"

# ProtoNord spesifikke innstillinger
PROTONORD_DIR="/home/kau005/prototype-workflow-med-github"
TEMP_DIR="/tmp/protonord_backup_temp"
BACKUP_NAME="protonord-website"
DATE=$(date +"%Y%m%d_%H%M%S")
YEAR=$(date +"%Y")
MONTH=$(date +"%m")
DAY=$(date +"%d")

# --- Finner riktige konfigurasjonsfiler ---
if [[ $EUID -eq 0 ]] && [[ -n "$SUDO_USER" ]]; then
  RCLONE_CONFIG_FILE="/home/$SUDO_USER/.config/rclone/rclone.conf"
  USER_HOME="/home/$SUDO_USER"
else
  RCLONE_CONFIG_FILE="$HOME/.config/rclone/rclone.conf"
  USER_HOME="$HOME"
fi

# Funksjon for logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$USER_HOME/protonord_backup.log"
}

# Funksjon for å rydde opp temp-mappen
cleanup() {
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
        log "Ryddet opp temp-mappe: $TEMP_DIR"
    fi
}

# Funksjon for å lage komplett backup
create_backup() {
    log "=== STARTER PROTONORD BACKUP ==="
    
    # Opprett temp-mappe
    mkdir -p "$TEMP_DIR"
    
    # Kopier hele prosjektmappen
    log "Kopierer ProtoNord website filer..."
    cp -r "$PROTONORD_DIR" "$TEMP_DIR/"
    
    # Lag en metadata-fil med backup-info
    cat > "$TEMP_DIR/backup_metadata.txt" << EOF
ProtoNord Website Backup
========================
Backup Date: $(date)
Source Directory: $PROTONORD_DIR
Backup Script: $0

Contents:
- Full website source code
- Shopify data files
- Documentation
- Configuration files
- Static assets (images, etc.)

Git Info:
$(cd "$PROTONORD_DIR" && git log --oneline -5 2>/dev/null || echo "Git info not available")

System Info:
Node Version: $(node --version 2>/dev/null || echo "Not installed")
NPM Version: $(npm --version 2>/dev/null || echo "Not installed")
EOF
    
    # Pakk sammen backupen
    BACKUP_FILENAME="${BACKUP_NAME}_${DATE}.tar.gz"
    log "Pakker backup: $BACKUP_FILENAME"
    
    cd "$TEMP_DIR"
    tar -czf "$BACKUP_FILENAME" prototype-workflow-med-github/ backup_metadata.txt
    
    # Sjekk at backup-filen ble opprettet
    if [[ ! -f "$TEMP_DIR/$BACKUP_FILENAME" ]]; then
        log "FEIL: Backup-fil ble ikke opprettet!"
        cleanup
        exit 1
    fi
    
    BACKUP_SIZE=$(du -h "$TEMP_DIR/$BACKUP_FILENAME" | cut -f1)
    log "Backup opprettet: $BACKUP_FILENAME (størrelse: $BACKUP_SIZE)"
}

# Funksjon for å laste opp til cloud
upload_to_clouds() {
    local backup_file="$TEMP_DIR/$BACKUP_FILENAME"
    
    # GFS-struktur: År/Måned/Dag
    local remote_dir_daily="$YEAR/$MONTH/$DAY"
    local remote_dir_weekly="$YEAR/Week_$(date +%U)"
    local remote_dir_monthly="$YEAR/$MONTH"
    
    # Bestem backup-type basert på dag i uke og måned
    local day_of_week=$(date +%u)  # 1=Monday, 7=Sunday
    local day_of_month=$(date +%d)
    
    local backup_type="daily"
    local remote_subdir="$remote_dir_daily"
    
    if [[ "$day_of_month" == "01" ]]; then
        backup_type="monthly"
        remote_subdir="$remote_dir_monthly"
    elif [[ "$day_of_week" == "7" ]]; then  # Sunday = weekly backup
        backup_type="weekly"
        remote_subdir="$remote_dir_weekly"
    fi
    
    log "Backup-type: $backup_type, Mappe: $remote_subdir"
    
    # Last opp til begge cloud-tjenester
    for remote_info in "$REMOTE_1_NAME:$REMOTE_1_BASE_DIR" "$REMOTE_2_NAME:$REMOTE_2_BASE_DIR"; do
        IFS=':' read -r remote_name remote_base <<< "$remote_info"
        
        log "Laster opp til $remote_name..."
        
        remote_path="$remote_name:$remote_base/$remote_subdir/"
        
        # Opprett mappe hvis den ikke eksisterer
        rclone mkdir "$remote_path" --config="$RCLONE_CONFIG_FILE"
        
        # Last opp backup
        if rclone copy "$backup_file" "$remote_path" --config="$RCLONE_CONFIG_FILE" --progress; then
            log "✅ Opplasting til $remote_name fullført"
        else
            log "❌ FEIL ved opplasting til $remote_name"
        fi
    done
}

# Funksjon for å slette gamle backuper (beholder siste 30 dager)
cleanup_old_backups() {
    log "Rydder gamle backuper..."
    
    for remote_info in "$REMOTE_1_NAME:$REMOTE_1_BASE_DIR" "$REMOTE_2_NAME:$REMOTE_2_BASE_DIR"; do
        IFS=':' read -r remote_name remote_base <<< "$remote_info"
        
        log "Rydder gamle backuper på $remote_name..."
        
        # List og slett filer eldre enn 30 dager (kun daily backuper)
        rclone delete "$remote_name:$remote_base" --min-age 30d --include "**/*daily*" --config="$RCLONE_CONFIG_FILE" || true
    done
}

# === HOVEDPROGRAM ===
trap cleanup EXIT

log "Starter ProtoNord backup prosess..."

# Sjekk at kildemappe eksisterer
if [[ ! -d "$PROTONORD_DIR" ]]; then
    log "FEIL: ProtoNord-mappen finnes ikke: $PROTONORD_DIR"
    exit 1
fi

# Sjekk at rclone er installert
if ! command -v rclone &> /dev/null; then
    log "FEIL: rclone er ikke installert!"
    exit 1
fi

# Sjekk at rclone-konfigurasjon finnes
if [[ ! -f "$RCLONE_CONFIG_FILE" ]]; then
    log "FEIL: Rclone-konfigurasjon finnes ikke: $RCLONE_CONFIG_FILE"
    exit 1
fi

# Kjør backup-prosessen
create_backup
upload_to_clouds
cleanup_old_backups

log "=== BACKUP FULLFØRT ==="
log "Backup-fil: $BACKUP_FILENAME"
log "Størrelse: $(du -h "$TEMP_DIR/$BACKUP_FILENAME" | cut -f1)"

cleanup