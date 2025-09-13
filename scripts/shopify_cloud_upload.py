#!/usr/bin/env python3
"""
ProtoNord Shopify Cloud Upload
Laster opp Shopify JSON data til cloud storage (Jottacloud primær, Google Drive backup)
"""

import json
import subprocess
import datetime
import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

def upload_to_cloud(json_file_path, cloud_folder="protonord/shopify"):
    """
    Upload JSON fil til begge cloud services
    Jottacloud = primær, Google Drive = backup
    Detekterer automatisk om fil er sensitiv basert på filnavn
    """
    if not Path(json_file_path).exists():
        logger.error(f"❌ JSON fil ikke funnet: {json_file_path}")
        return False
    
    # Sjekk om dette er en sensitiv fil
    filename = Path(json_file_path).name
    is_sensitive = "sensitive" in filename
    
    # Generer filnavn med timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Bestem cloud paths basert på filtype
    if is_sensitive:
        # Sensitive filer går til egen mappe
        cloud_files = {
            'latest': f"{cloud_folder}/sensitive/protonord_shopify_sensitive_latest.json",
            'timestamped': f"{cloud_folder}/sensitive/archive/protonord_shopify_sensitive_{timestamp}.json"
        }
        logger.info(f"🔒 Uploading sensitive data (kun cloud storage)")
    else:
        # Public filer til standard mappe
        cloud_files = {
            'latest': f"{cloud_folder}/protonord_shopify_latest.json",
            'timestamped': f"{cloud_folder}/archive/protonord_shopify_data_{timestamp}.json"
        }
        logger.info(f"🌐 Uploading public data")
    
    success_count = 0
    total_uploads = 0
    
    # Upload til begge clouds
    for cloud_name, remote in [("Jottacloud", "jottacloud"), ("Google Drive", "gdrive")]:
        logger.info(f"☁️ Uploader til {cloud_name}...")
        
        for file_type, cloud_path in cloud_files.items():
            try:
                # Opprett directory først
                cloud_dir = str(Path(cloud_path).parent)
                mkdir_cmd = f"rclone mkdir {remote}:{cloud_dir}"
                subprocess.run(mkdir_cmd, shell=True, capture_output=True, check=False)
                
                # Upload fil
                upload_cmd = f"rclone copy '{json_file_path}' {remote}:{cloud_dir} --progress"
                result = subprocess.run(upload_cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"✅ {cloud_name} {file_type}: {cloud_path}")
                    success_count += 1
                else:
                    logger.error(f"❌ {cloud_name} {file_type} feilet: {result.stderr}")
                
                total_uploads += 1
                
                # Hvis dette er latest filen, endre navn
                if file_type == 'timestamped':
                    # Kopier til latest navn
                    latest_cmd = f"rclone copy {remote}:{cloud_path} {remote}:{Path(cloud_files['latest']).parent}/ --progress"
                    result2 = subprocess.run(latest_cmd, shell=True, capture_output=True)
                    
                    # Rename til latest (bruk faktisk filnavn fra json_file_path)
                    uploaded_filename = Path(json_file_path).name
                    move_cmd = f"rclone moveto {remote}:{Path(cloud_files['latest']).parent}/{uploaded_filename} {remote}:{cloud_files['latest']}"
                    subprocess.run(move_cmd, shell=True, capture_output=True)
                
            except Exception as e:
                logger.error(f"❌ {cloud_name} upload feil: {e}")
                total_uploads += 1
    
    logger.info(f"📊 Cloud upload resultat: {success_count}/{total_uploads} vellykkede uploads")
    return success_count > 0

def cleanup_old_files(days_to_keep=7):
    """Slett gamle lokale Shopify JSON filer"""
    data_dir = Path(__file__).parent.parent / "data/shopify"
    if not data_dir.exists():
        return
    
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_to_keep)
    deleted_count = 0
    
    for json_file in data_dir.glob("protonord_shopify_data_*.json"):
        try:
            # Sjekk filens alder
            file_age = datetime.datetime.fromtimestamp(json_file.stat().st_mtime)
            if file_age < cutoff_date:
                json_file.unlink()
                deleted_count += 1
                logger.info(f"🗑️ Slettet gammel fil: {json_file.name}")
        except Exception as e:
            logger.warning(f"Kunne ikke slette {json_file.name}: {e}")
    
    if deleted_count > 0:
        logger.info(f"🧹 Slettet {deleted_count} gamle filer")

if __name__ == "__main__":
    # Test upload med siste JSON fil
    data_dir = Path(__file__).parent.parent / "data/shopify"
    latest_file = data_dir / "protonord_shopify_latest.json"
    
    if latest_file.exists():
        print(f"🧪 Tester upload av {latest_file}")
        success = upload_to_cloud(latest_file)
        if success:
            print("✅ Test upload fullført!")
        else:
            print("❌ Test upload feilet!")
    else:
        print(f"❌ Ingen JSON fil å teste med: {latest_file}")
        print("Kjør først: python3 scripts/shopify_sync.py")