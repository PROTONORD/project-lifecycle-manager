#!/usr/bin/env python3
"""
ProtoNord Sync Dashboard
Viser status for automatisk synkronisering
"""

import json
import os
import datetime
from pathlib import Path
import subprocess

def get_sync_status():
    """Sjekk status for synkronisering"""
    script_dir = Path(__file__).parent.parent
    data_file = script_dir / "static/data/protonord_cloud_data.json"
    log_dir = script_dir / "logs"
    
    status = {
        "last_sync": "Aldri",
        "total_files": 0,
        "clouds": {},
        "cron_active": False,
        "recent_logs": []
    }
    
    # Sjekk siste sync
    if data_file.exists():
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            last_updated = data.get("last_updated", "")
            if last_updated:
                dt = datetime.datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                status["last_sync"] = dt.strftime("%Y-%m-%d %H:%M:%S")
            
            # Tell filer per cloud
            for cloud_name, cloud_data in data.get("clouds", {}).items():
                file_count = len(cloud_data.get("protonord_files", []))
                status["clouds"][cloud_name] = file_count
                status["total_files"] += file_count
                
        except Exception as e:
            print(f"Feil ved lesing av sync data: {e}")
    
    # Sjekk cron status
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0 and 'automated_protonord_sync.py' in result.stdout:
            status["cron_active"] = True
    except:
        pass
    
    # Hent siste logs
    if log_dir.exists():
        log_files = sorted(log_dir.glob("protonord_sync_*.log"), reverse=True)
        for log_file in log_files[:3]:  # Siste 3 log filer
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Ta siste 5 linjer
                    recent_lines = lines[-5:] if len(lines) >= 5 else lines
                    status["recent_logs"].append({
                        "file": log_file.name,
                        "lines": [line.strip() for line in recent_lines]
                    })
            except:
                pass
    
    return status

def print_dashboard():
    """Vis dashboard"""
    status = get_sync_status()
    
    print("=" * 60)
    print("🚀 PROTONORD CLOUD SYNC DASHBOARD")
    print("=" * 60)
    
    # Sync status
    print(f"📅 Siste synkronisering: {status['last_sync']}")
    print(f"📁 Totalt antall filer: {status['total_files']}")
    
    # Cloud status
    print("\n☁️ CLOUD STATUS:")
    for cloud, count in status['clouds'].items():
        print(f"   {cloud}: {count} filer")
    
    # Cron status
    cron_emoji = "✅" if status['cron_active'] else "❌"
    print(f"\n🕒 Automatisk synkronisering: {cron_emoji}")
    
    # Recent logs
    if status['recent_logs']:
        print("\n📋 SISTE LOGGER:")
        for log in status['recent_logs'][:1]:  # Vis bare den nyeste
            print(f"   📄 {log['file']}:")
            for line in log['lines'][-3:]:  # Siste 3 linjer
                if line:
                    print(f"      {line}")
    
    print("\n" + "=" * 60)
    print("📘 KOMMANDOER:")
    print("   - Manuell sync: python3 scripts/automated_protonord_sync.py")
    print("   - Se alle logs: ls -la logs/")
    print("   - Cron status: crontab -l")
    print("   - Setup cron: ./scripts/setup_cron.sh")
    print("=" * 60)

if __name__ == "__main__":
    print_dashboard()