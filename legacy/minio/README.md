# Legacy MinIO Files

This folder contains legacy files from when the system used MinIO for object storage.

The system has been migrated to use cloud storage (Google Drive and Jottacloud) via rclone for better reliability and cost-effectiveness.

## Migrated Components:

- **minio_client.py**: Legacy MinIO client code
- **setup/**: MinIO server installation and configuration files
- **tools/**: MinIO-specific utility tools

## Current Architecture:

The system now uses:
- **rclone** for cloud storage management
- **Google Drive** as primary cloud storage
- **Jottacloud** as secondary backup
- **protonord_cloud_backup.sh** for automated backups

## Migration Notes:

All functionality has been preserved, but the storage backend has been modernized to use cloud-native solutions instead of self-hosted MinIO.
