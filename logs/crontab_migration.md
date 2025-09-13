# Crontab Update Log

## Endringer gjort 2025-09-13

### Bakgrunn
Mappenavn endret fra `prototype-workflow-med-github` til `project-lifecycle-manager` 
for å matche GitHub repository navn.

### Cronjobs oppdatert:

1. **Automatisk Protonord sync (daglig kl 02:00)**
   - Før: `cd /home/kau005/prototype-workflow-med-github && /usr/bin/python3 /home/kau005/prototype-workflow-med-github/scripts/automated_protonord_sync.py`
   - Etter: `cd /home/kau005/project-lifecycle-manager && /usr/bin/python3 /home/kau005/project-lifecycle-manager/scripts/automated_protonord_sync.py`

2. **Cloud backup (daglig kl 01:30)**
   - Før: `/home/kau005/prototype-workflow-med-github/scripts/protonord_cloud_backup.sh`
   - Etter: `/home/kau005/project-lifecycle-manager/scripts/protonord_cloud_backup.sh`

### Verifisering
- ✅ Alle stier oppdatert
- ✅ Cronjobs teste og fungerer
- ✅ Ingen brutte referanser til gammel mappe

### Aktuelle cronjobs:
```
0 3 * * 0 /home/kau005/backup_docker.sh >> /mnt/nextcloud_backups/docker_backups/backup.log 2>&1
0 2 * * * cd /home/kau005/project-lifecycle-manager && /usr/bin/python3 /home/kau005/project-lifecycle-manager/scripts/automated_protonord_sync.py >> /home/kau005/project-lifecycle-manager/logs/cron.log 2>&1
30 1 * * * /home/kau005/project-lifecycle-manager/scripts/protonord_cloud_backup.sh >> /home/kau005/protonord_backup.log 2>&1
```