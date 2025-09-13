#!/usr/bin/env python3
"""
Cloud File Sync and Mapping Script
Synkroniserer filstrukturer fra Jottacloud og Google Drive til JSON-format
for visning i Docusaurus wiki.
"""

import json
import subprocess
import os
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudFileMapper:
    def __init__(self, output_dir="static/data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def run_rclone_command(self, cmd):
        """Kjør rclone kommando og returner output"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"rclone kommando feilet: {e}")
            return None
    
    def parse_rclone_ls(self, output):
        """Parse rclone ls output til strukturert format"""
        files = []
        for line in output.strip().split('\n'):
            if line.strip():
                parts = line.strip().split(None, 3)
                if len(parts) >= 4:
                    size, date, time, path = parts[0], parts[1], parts[2], parts[3]
                    files.append({
                        'path': path,
                        'size': int(size) if size.isdigit() else 0,
                        'modified': f"{date} {time}",
                        'type': 'file' if '.' in Path(path).name else 'folder'
                    })
        return files
    
    def get_file_structure(self, remote_name, max_depth=3):
        """Hent filstruktur fra rclone remote"""
        logger.info(f"Henter filstruktur fra {remote_name}")
        
        # Få liste over alle filer
        cmd = f"rclone ls {remote_name}: --max-depth {max_depth}"
        output = self.run_rclone_command(cmd)
        
        if not output:
            return []
        
        files = self.parse_rclone_ls(output)
        
        # Organiser i mappestruktur
        structure = self.organize_files_by_folder(files)
        
        return structure
    
    def organize_files_by_folder(self, files):
        """Organiser filer i mappestruktur"""
        folders = {}
        
        for file_info in files:
            path_parts = Path(file_info['path']).parts
            
            # Bygg mappestruktur
            current_level = folders
            for i, part in enumerate(path_parts[:-1]):
                if part not in current_level:
                    current_level[part] = {
                        'type': 'folder',
                        'files': [],
                        'subfolders': {}
                    }
                current_level = current_level[part]['subfolders']
            
            # Legg til fil i siste mappe
            folder_path = '/'.join(path_parts[:-1]) if len(path_parts) > 1 else ''
            file_name = path_parts[-1]
            
            if folder_path:
                # Naviger til riktig mappe
                current_level = folders
                for part in Path(folder_path).parts:
                    current_level = current_level[part]['subfolders']
                
                if 'files' not in current_level:
                    current_level['files'] = []
                
                parent_folder = folders
                for part in Path(folder_path).parts[:-1]:
                    parent_folder = parent_folder[part]['subfolders']
                
                folder_name = Path(folder_path).parts[-1]
                if folder_name not in parent_folder:
                    parent_folder[folder_name] = {
                        'type': 'folder',
                        'files': [],
                        'subfolders': {}
                    }
                
                parent_folder[folder_name]['files'].append({
                    'name': file_name,
                    'size': file_info['size'],
                    'modified': file_info['modified'],
                    'path': file_info['path']
                })
            else:
                # Fil i root
                if 'root_files' not in folders:
                    folders['root_files'] = []
                folders['root_files'].append({
                    'name': file_name,
                    'size': file_info['size'],
                    'modified': file_info['modified'],
                    'path': file_info['path']
                })
        
        return folders
    
    def sync_cloud_data(self):
        """Synkroniser data fra alle cloud-tjenester"""
        logger.info("Starter synkronisering av cloud-data")
        
        cloud_data = {
            'last_updated': datetime.now().isoformat(),
            'clouds': {}
        }
        
        # Synkroniser Jottacloud
        logger.info("Synkroniserer Jottacloud...")
        jottacloud_data = self.get_file_structure('jottacloud')
        cloud_data['clouds']['jottacloud'] = {
            'name': 'Jottacloud',
            'structure': jottacloud_data,
            'last_sync': datetime.now().isoformat()
        }
        
        # Synkroniser Google Drive
        logger.info("Synkroniserer Google Drive...")
        gdrive_data = self.get_file_structure('gdrive')
        cloud_data['clouds']['gdrive'] = {
            'name': 'Google Drive',
            'structure': gdrive_data,
            'last_sync': datetime.now().isoformat()
        }
        
        # Lagre til JSON
        output_file = self.output_dir / 'cloud_structure.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cloud_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Cloud-data lagret til {output_file}")
        return cloud_data

def main():
    """Hovedfunksjon"""
    mapper = CloudFileMapper()
    
    try:
        data = mapper.sync_cloud_data()
        print(f"✅ Synkronisering fullført!")
        print(f"📁 Jottacloud: {len(data['clouds']['jottacloud']['structure'])} mapper")
        print(f"📁 Google Drive: {len(data['clouds']['gdrive']['structure'])} mapper")
        print(f"🕐 Sist oppdatert: {data['last_updated']}")
        
    except Exception as e:
        logger.error(f"Feil under synkronisering: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())