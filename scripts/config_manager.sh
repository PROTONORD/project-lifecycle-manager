#!/bin/bash

# ===========================================
# CONFIG MANAGER - Universal Configuration Tool
# ===========================================
# Brukes for å legge til/fjerne innhold i ulike konfigurasjonsfiler
# Støtter: crontab, YAML, JSON, conf-filer, osv.

# Standardverdier
CONFIG_TYPE=""
ACTION=""
CONTENT=""
BACKUP_DIR="$HOME/.config_backups"
VERBOSE=false

# Farger for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging funksjon
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        "ERROR")
            echo -e "${RED}[ERROR]${NC} $message" >&2
            echo "[$timestamp] ERROR: $message" >> "$HOME/config_manager.log"
            ;;
        "SUCCESS")
            echo -e "${GREEN}[SUCCESS]${NC} $message"
            echo "[$timestamp] SUCCESS: $message" >> "$HOME/config_manager.log"
            ;;
        "INFO")
            echo -e "${BLUE}[INFO]${NC} $message"
            if [ "$VERBOSE" = true ]; then
                echo "[$timestamp] INFO: $message" >> "$HOME/config_manager.log"
            fi
            ;;
        "WARNING")
            echo -e "${YELLOW}[WARNING]${NC} $message"
            echo "[$timestamp] WARNING: $message" >> "$HOME/config_manager.log"
            ;;
    esac
}

# Hjelpefunksjon
show_help() {
    cat << EOF
CONFIG MANAGER - Universal Configuration Tool

BRUK:
    $0 [OPSJONER] ACTION CONFIG_TYPE [CONTENT]

ACTIONS:
    add         Legg til innhold i konfigurasjon
    remove      Fjern innhold fra konfigurasjon
    backup      Lag backup av konfigurasjon
    restore     Gjenopprett fra backup
    show        Vis nåværende konfigurasjon

CONFIG_TYPES:
    crontab     Crontab-oppføringer
    yaml        YAML-filer
    json        JSON-filer
    conf        Generelle konfigurasjonsfiler
    env         Environment-filer
    hosts       /etc/hosts
    nginx       Nginx-konfigurasjon
    apache      Apache-konfigurasjon

OPSJONER:
    -f FILE     Spesifiser fil (for yaml, json, conf, etc.)
    -b          Lag backup før endring
    -v          Verbose output
    -d          Dry run (vis hva som ville skjedd)
    -h          Vis denne hjelpen

EKSEMPLER:
    # Legg til cron-jobb
    $0 add crontab "30 1 * * * /path/to/script.sh"
    
    # Legg til YAML-oppføring
    $0 -f config.yml add yaml "new_setting: value"
    
    # Backup crontab
    $0 backup crontab
    
    # Vis crontab
    $0 show crontab

EOF
}

# Lag backup-mappe
ensure_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        log "INFO" "Opprettet backup-mappe: $BACKUP_DIR"
    fi
}

# Backup-funksjon
create_backup() {
    local config_type=$1
    local file_path=$2
    local backup_name=""
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    
    ensure_backup_dir
    
    case $config_type in
        "crontab")
            backup_name="crontab_${timestamp}.backup"
            crontab -l > "$BACKUP_DIR/$backup_name" 2>/dev/null
            ;;
        "yaml"|"json"|"conf"|"env")
            if [ -z "$file_path" ]; then
                log "ERROR" "Fil-sti kreves for $config_type"
                return 1
            fi
            backup_name="$(basename $file_path)_${timestamp}.backup"
            cp "$file_path" "$BACKUP_DIR/$backup_name"
            ;;
        "hosts")
            backup_name="hosts_${timestamp}.backup"
            sudo cp /etc/hosts "$BACKUP_DIR/$backup_name"
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        log "SUCCESS" "Backup opprettet: $BACKUP_DIR/$backup_name"
        echo "$BACKUP_DIR/$backup_name"
    else
        log "ERROR" "Kunne ikke opprette backup"
        return 1
    fi
}

# Legg til innhold
add_content() {
    local config_type=$1
    local content=$2
    local file_path=$3
    
    case $config_type in
        "crontab")
            # Sjekk om oppføringen allerede eksisterer
            if crontab -l 2>/dev/null | grep -F "$content" > /dev/null; then
                log "WARNING" "Cron-oppføring eksisterer allerede"
                return 1
            fi
            
            # Legg til ny oppføring
            (crontab -l 2>/dev/null; echo "$content") | crontab -
            log "SUCCESS" "Lagt til cron-oppføring: $content"
            ;;
            
        "yaml")
            if [ -z "$file_path" ]; then
                log "ERROR" "Fil-sti kreves for YAML"
                return 1
            fi
            echo "$content" >> "$file_path"
            log "SUCCESS" "Lagt til YAML-innhold i $file_path"
            ;;
            
        "json")
            if [ -z "$file_path" ]; then
                log "ERROR" "Fil-sti kreves for JSON"
                return 1
            fi
            # For JSON kreves mer sofistikert håndtering
            log "WARNING" "JSON-redigering krever manuell implementering"
            ;;
            
        "conf"|"env")
            if [ -z "$file_path" ]; then
                log "ERROR" "Fil-sti kreves for $config_type"
                return 1
            fi
            echo "$content" >> "$file_path"
            log "SUCCESS" "Lagt til innhold i $file_path"
            ;;
            
        "hosts")
            echo "$content" | sudo tee -a /etc/hosts > /dev/null
            log "SUCCESS" "Lagt til hosts-oppføring: $content"
            ;;
    esac
}

# Fjern innhold
remove_content() {
    local config_type=$1
    local content=$2
    local file_path=$3
    
    case $config_type in
        "crontab")
            crontab -l 2>/dev/null | grep -v -F "$content" | crontab -
            log "SUCCESS" "Fjernet cron-oppføring: $content"
            ;;
            
        "yaml"|"conf"|"env")
            if [ -z "$file_path" ]; then
                log "ERROR" "Fil-sti kreves for $config_type"
                return 1
            fi
            sed -i.bak "/$content/d" "$file_path"
            log "SUCCESS" "Fjernet innhold fra $file_path"
            ;;
            
        "hosts")
            sudo sed -i.bak "/$content/d" /etc/hosts
            log "SUCCESS" "Fjernet hosts-oppføring: $content"
            ;;
    esac
}

# Vis konfigurasjon
show_config() {
    local config_type=$1
    local file_path=$2
    
    case $config_type in
        "crontab")
            log "INFO" "Nåværende crontab:"
            crontab -l 2>/dev/null || log "WARNING" "Ingen crontab funnet"
            ;;
            
        "yaml"|"json"|"conf"|"env")
            if [ -z "$file_path" ]; then
                log "ERROR" "Fil-sti kreves for $config_type"
                return 1
            fi
            log "INFO" "Innhold i $file_path:"
            cat "$file_path" 2>/dev/null || log "ERROR" "Kunne ikke lese $file_path"
            ;;
            
        "hosts")
            log "INFO" "Nåværende hosts-fil:"
            cat /etc/hosts
            ;;
    esac
}

# Gjenopprett fra backup
restore_backup() {
    local config_type=$1
    local backup_file=$2
    
    if [ -z "$backup_file" ]; then
        log "INFO" "Tilgjengelige backuper:"
        ls -la "$BACKUP_DIR" | grep "$config_type"
        return
    fi
    
    if [ ! -f "$BACKUP_DIR/$backup_file" ]; then
        log "ERROR" "Backup-fil ikke funnet: $BACKUP_DIR/$backup_file"
        return 1
    fi
    
    case $config_type in
        "crontab")
            crontab "$BACKUP_DIR/$backup_file"
            log "SUCCESS" "Gjenopprettet crontab fra $backup_file"
            ;;
        *)
            log "WARNING" "Gjenoppretting for $config_type må gjøres manuelt"
            log "INFO" "Backup-fil: $BACKUP_DIR/$backup_file"
            ;;
    esac
}

# Parse kommandolinje-argumenter
while getopts "f:bvdh" opt; do
    case $opt in
        f) FILE_PATH="$OPTARG" ;;
        b) CREATE_BACKUP=true ;;
        v) VERBOSE=true ;;
        d) DRY_RUN=true ;;
        h) show_help; exit 0 ;;
        *) show_help; exit 1 ;;
    esac
done

shift $((OPTIND-1))

# Sjekk argumenter
if [ $# -lt 2 ]; then
    log "ERROR" "For få argumenter"
    show_help
    exit 1
fi

ACTION=$1
CONFIG_TYPE=$2
CONTENT=$3

# Utfør handling
case $ACTION in
    "add")
        if [ -z "$CONTENT" ]; then
            log "ERROR" "Innhold kreves for 'add' handling"
            exit 1
        fi
        
        if [ "$CREATE_BACKUP" = true ]; then
            create_backup "$CONFIG_TYPE" "$FILE_PATH"
        fi
        
        if [ "$DRY_RUN" = true ]; then
            log "INFO" "DRY RUN: Ville lagt til '$CONTENT' i $CONFIG_TYPE"
        else
            add_content "$CONFIG_TYPE" "$CONTENT" "$FILE_PATH"
        fi
        ;;
        
    "remove")
        if [ -z "$CONTENT" ]; then
            log "ERROR" "Innhold kreves for 'remove' handling"
            exit 1
        fi
        
        if [ "$CREATE_BACKUP" = true ]; then
            create_backup "$CONFIG_TYPE" "$FILE_PATH"
        fi
        
        if [ "$DRY_RUN" = true ]; then
            log "INFO" "DRY RUN: Ville fjernet '$CONTENT' fra $CONFIG_TYPE"
        else
            remove_content "$CONFIG_TYPE" "$CONTENT" "$FILE_PATH"
        fi
        ;;
        
    "backup")
        create_backup "$CONFIG_TYPE" "$FILE_PATH"
        ;;
        
    "restore")
        restore_backup "$CONFIG_TYPE" "$CONTENT"
        ;;
        
    "show")
        show_config "$CONFIG_TYPE" "$FILE_PATH"
        ;;
        
    *)
        log "ERROR" "Ukjent handling: $ACTION"
        show_help
        exit 1
        ;;
esac

log "INFO" "Handling '$ACTION' fullført for $CONFIG_TYPE"