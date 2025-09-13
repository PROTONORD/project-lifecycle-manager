#!/bin/bash
# ProtoNord Cloud Sync - Cron Setup Script

SCRIPT_DIR="/home/kau005/project-lifecycle-manager"
SYNC_SCRIPT="$SCRIPT_DIR/scripts/automated_protonord_sync.py"
LOG_DIR="$SCRIPT_DIR/logs"

# Opprett logs directory
mkdir -p "$LOG_DIR"

# Backup eksisterende crontab
echo "🔄 Backup eksisterende crontab..."
crontab -l > "$LOG_DIR/crontab_backup_$(date +%Y%m%d_%H%M%S).txt" 2>/dev/null || echo "Ingen eksisterende crontab"

# Sjekk om cron job allerede eksisterer
if crontab -l 2>/dev/null | grep -q "automated_protonord_sync.py"; then
    echo "⚠️ ProtoNord cron job eksisterer allerede!"
    echo "Eksisterende cron jobs:"
    crontab -l | grep "automated_protonord_sync.py"
    echo ""
    read -p "Vil du oppdatere eksisterende cron job? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Avbryter..."
        exit 1
    fi
    # Fjern eksisterende cron job
    crontab -l | grep -v "automated_protonord_sync.py" | crontab -
fi

# Legg til ny cron job
echo "📅 Legger til automatisk ProtoNord synkronisering..."

# Kjører hver natt kl 02:00
CRON_ENTRY="0 2 * * * cd $SCRIPT_DIR && /usr/bin/python3 $SYNC_SCRIPT >> $LOG_DIR/cron.log 2>&1"

# Legg til i crontab
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ Cron job lagt til!"
echo "📋 Synkronisering vil kjøre hver natt kl 02:00"
echo "📂 Logs lagres i: $LOG_DIR"

# Vis aktive cron jobs
echo ""
echo "🔍 Aktive cron jobs:"
crontab -l

# Test scriptet
echo ""
echo "🧪 Vil du teste sync-scriptet nå? (y/n): "
read -p "" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Kjører test..."
    cd "$SCRIPT_DIR"
    python3 "$SYNC_SCRIPT"
fi

echo ""
echo "🎉 Automatisk synkronisering er satt opp!"
echo "📘 Kommandoer:"
echo "   - Se cron status: sudo systemctl status cron"
echo "   - Se cron logs: tail -f $LOG_DIR/cron.log"
echo "   - Manuell sync: cd $SCRIPT_DIR && python3 $SYNC_SCRIPT"
echo "   - Fjern cron job: crontab -e"