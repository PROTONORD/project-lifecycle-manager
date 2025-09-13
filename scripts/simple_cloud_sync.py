#!/usr/bin/enlogging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_protonord_structure(remote):Enklere Cloud File Sync Script
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

def run_rclone_tree(remote):
    """Få filstruktur med rclone tree"""
    try:
        cmd = f"rclone tree {remote}: --human-readable --dirs-only --max-depth 3"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"rclone tree feilet for {remote}: {e}")
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

def get_protonord_structure(remote):
    """Få filstruktur for protonord-mappen"""
    try:
        cmd = f"rclone tree {remote}:protonord --human-readable --max-depth 5"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"rclone tree feilet for {remote}:protonord: {e}")
        return None

def sync_cloud_structure():
    """Synkroniser cloud-strukturer"""
    logger.info("Starter cloud-synkronisering...")
    
    output_dir = Path("static/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cloud_data = {
        'last_updated': datetime.now().isoformat(),
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
    output_file = output_dir / 'cloud_structure.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cloud_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Data lagret til {output_file}")
    print(f"✅ Synkronisering fullført! Data lagret til {output_file}")

if __name__ == "__main__":
    sync_cloud_structure()