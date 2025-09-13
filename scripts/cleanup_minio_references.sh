#!/bin/bash

# Script for å fjerne MinIO-referanser fra catalog README-filer
# Erstatter alle MinIO-lenker med cloud backup referanser

WORKSPACE_ROOT="/home/kau005/prototype-workflow-med-github"
CATALOG_DIR="${WORKSPACE_ROOT}/catalog"
BACKUP_DIR="${WORKSPACE_ROOT}/backup_original_readmes"
LOG_FILE="${WORKSPACE_ROOT}/minio_cleanup.log"

# Opprett backup-mappe
mkdir -p "$BACKUP_DIR"

# Start logg
echo "MinIO cleanup startet: $(date)" > "$LOG_FILE"
echo "Workspace: $WORKSPACE_ROOT" >> "$LOG_FILE"
echo "=" >> "$LOG_FILE"

# Finn alle README-filer som inneholder MinIO-referanser
echo "Søker etter filer med MinIO-referanser..."
FILES_WITH_MINIO=$(find "$CATALOG_DIR" -name "README.md" -exec grep -l "MinIO\|minio" {} \;)

if [ -z "$FILES_WITH_MINIO" ]; then
    echo "Ingen filer med MinIO-referanser funnet."
    exit 0
fi

FILE_COUNT=$(echo "$FILES_WITH_MINIO" | wc -l)
echo "Fant $FILE_COUNT filer med MinIO-referanser"
echo "Fant $FILE_COUNT filer med MinIO-referanser" >> "$LOG_FILE"

# Backup og oppdater hver fil
counter=0
for file in $FILES_WITH_MINIO; do
    counter=$((counter + 1))
    echo "Behandler fil $counter/$FILE_COUNT: $file"
    
    # Lag backup
    backup_path="$BACKUP_DIR/$(basename "$file")_$(date +%Y%m%d_%H%M%S)_$counter"
    cp "$file" "$backup_path"
    
    # Lag relativt path for logging
    rel_path="${file#$WORKSPACE_ROOT/}"
    echo "  Fil: $rel_path" >> "$LOG_FILE"
    echo "  Backup: $backup_path" >> "$LOG_FILE"
    
    # Erstatt MinIO-referanser
    sed -i 's|minio\.protonord\.no/[^)]*|cloud backup repository|g' "$file"
    sed -i 's|MinIO storage|cloud backup system|g' "$file"
    sed -i 's|MinIO object storage|cloud backup repository|g' "$file"
    sed -i 's|MinIO|cloud backup|g' "$file"
    sed -i 's|minio|cloud backup|g' "$file"
    
    # Erstatt spesifikke URL-mønstre
    sed -i 's|https://minio\.protonord\.no/[^)]*|cloud backup repository|g' "$file"
    sed -i 's|http://minio\.protonord\.no/[^)]*|cloud backup repository|g' "$file"
    
    # Erstatt markdown lenker med MinIO
    sed -i 's|\[.*\](.*minio.*)|[Tilgjengelig i cloud backup](cloud-backup)|g' "$file"
    
    # Oppdater bilder og CAD-referanser
    sed -i 's|!\[.*\](.*minio.*)|![Image tilgjengelig i cloud backup](cloud-backup)|g' "$file"
    
    echo "    - Oppdatert med cloud backup referanser" >> "$LOG_FILE"
done

echo ""
echo "Cleanup fullført!"
echo "- Behandlet $FILE_COUNT filer"
echo "- Backup-filer lagret i: $BACKUP_DIR"
echo "- Logg tilgjengelig i: $LOG_FILE"
echo ""
echo "Cleanup fullført: $(date)" >> "$LOG_FILE"
echo "Behandlet $FILE_COUNT filer totalt" >> "$LOG_FILE"

# Vis sammendrag
echo "Sammendrag:"
echo "- Alle MinIO URL-er erstattet med 'cloud backup repository'"
echo "- MinIO-referanser erstattet med 'cloud backup'"
echo "- Backup-filer opprettet for alle endrede filer"