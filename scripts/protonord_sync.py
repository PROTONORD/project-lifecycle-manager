#!/usr/bin/env python3
"""
ProtoNord Cloud Sync Script
Henter filstrukturer fra protonord-mapper i Jottacloud og Google Drive
"""

import json
import subprocess
import os
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_protonord_structure(remote):
    """Få filstruktur for protonord-mappen"""
    try:
        cmd = f"rclone tree {remote}:protonord --human-readable --max-depth 5"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"rclone tree feilet for {remote}:protonord: {e}")
        return None

def get_file_list(remote, path="protonord"):
    """Få filliste for protonord-mappen"""
    try:
        cmd = f"rclone lsjson {remote}:{path} --human-readable --recursive"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"rclone lsjson feilet for {remote}:{path}: {e}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode feilet: {e}")
        return []

def sync_protonord_data():
    """Synkroniser data fra protonord-mapper"""
    logger.info("Starter synkronisering av ProtoNord cloud-data...")
    
    output_dir = Path("static/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cloud_data = {
        'last_updated': datetime.now().isoformat(),
        'organization': 'ProtoNord',
        'clouds': {}
    }
    
    # Synkroniser hver cloud-tjeneste
    for remote in ['jottacloud', 'gdrive']:
        logger.info(f"Synkroniserer {remote}:protonord...")
        
        # Få mappestruktur for protonord-mappen
        tree_output = get_protonord_structure(remote)
        
        # Få fullstendig filliste for protonord-mappen  
        files = get_file_list(remote, "protonord")
        
        cloud_data['clouds'][remote] = {
            'name': 'Jottacloud' if remote == 'jottacloud' else 'Google Drive',
            'tree_structure': tree_output,
            'protonord_files': files,
            'base_path': 'protonord',
            'last_sync': datetime.now().isoformat()
        }
    
    # Lagre til JSON
    output_file = output_dir / 'protonord_cloud_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cloud_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"ProtoNord data lagret til {output_file}")
    
    # Statistikk
    jotta_files = len(cloud_data['clouds']['jottacloud']['protonord_files'])
    gdrive_files = len(cloud_data['clouds']['gdrive']['protonord_files'])
    
    print(f"✅ ProtoNord synkronisering fullført!")
    print(f"📁 Jottacloud/protonord: {jotta_files} filer")
    print(f"📁 Google Drive/protonord: {gdrive_files} filer")
    print(f"🕐 Sist oppdatert: {cloud_data['last_updated']}")
    print(f"💾 Data lagret til: {output_file}")

if __name__ == "__main__":
    sync_protonord_data()