#!/usr/bin/env python3
"""
Automatisert ProtoNord Cloud Synkronisering
Kjører hver natt for å synkronisere cloud-filer til Docusaurus wiki.
"""

import json
import subprocess
import datetime
import logging
import os
import sys
from pathlib import Path

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"protonord_sync_{datetime.date.today()}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def run_command(cmd, description):
    """Kjør en kommando og logg resultatet"""
    try:
        logger.info(f"Kjører: {description}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            logger.info(f"✅ {description} fullført")
            return True, result.stdout
        else:
            logger.error(f"❌ {description} feilet: {result.stderr}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        logger.error(f"⏰ {description} timed out (5 min)")
        return False, "Timeout"
    except Exception as e:
        logger.error(f"💥 {description} kastet exception: {e}")
        return False, str(e)

def get_protonord_structure(remote):
    """Hent protonord folder struktur fra cloud"""
    cmd = f"rclone lsjson --recursive {remote}:protonord"
    success, output = run_command(cmd, f"Synkroniserer {remote}:protonord")
    
    if not success:
        return [], ""
    
    try:
        files = json.loads(output) if output.strip() else []
        # Generer tree struktur
        tree_cmd = f"rclone tree {remote}:protonord"
        tree_success, tree_output = run_command(tree_cmd, f"Genererer tree for {remote}")
        tree_structure = tree_output if tree_success else "Tree ikke tilgjengelig"
        
        return files, tree_structure
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing feil for {remote}: {e}")
        return [], ""

def sync_protonord_data():
    """Hovedfunksjon for å synkronisere ProtoNord data"""
    logger.info("🚀 Starter automatisk ProtoNord synkronisering...")
    
    # Sjekk at vi er i rett directory
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    logger.info(f"Working directory: {os.getcwd()}")
    
    # Test rclone tilkobling
    success, _ = run_command("rclone version", "Test rclone")
    if not success:
        logger.error("❌ rclone ikke tilgjengelig")
        return False
    
    # Hent data fra begge clouds
    clouds_data = {}
    
    # Jottacloud
    jotta_files, jotta_tree = get_protonord_structure("jottacloud")
    clouds_data["jottacloud"] = {
        "name": "Jottacloud",
        "tree_structure": jotta_tree,
        "protonord_files": jotta_files
    }
    
    # Google Drive
    gdrive_files, gdrive_tree = get_protonord_structure("gdrive")
    clouds_data["gdrive"] = {
        "name": "Google Drive", 
        "tree_structure": gdrive_tree,
        "protonord_files": gdrive_files
    }
    
    # Lag komplett data struktur
    protonord_data = {
        "last_updated": datetime.datetime.now().isoformat(),
        "sync_mode": "automated",
        "organization": "ProtoNord",
        "clouds": clouds_data
    }
    
    # Lagre til JSON fil
    output_file = Path("static/data/protonord_cloud_data.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(protonord_data, f, indent=2, ensure_ascii=False)
        
        total_files = len(jotta_files) + len(gdrive_files)
        logger.info(f"✅ ProtoNord synkronisering fullført!")
        logger.info(f"📁 Jottacloud/protonord: {len(jotta_files)} filer")
        logger.info(f"📁 Google Drive/protonord: {len(gdrive_files)} filer")
        logger.info(f"📊 Totalt: {total_files} filer")
        logger.info(f"💾 Data lagret til: {output_file}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Feil ved lagring av data: {e}")
        return False

def restart_docusaurus():
    """Restart Docusaurus for å laste nye data"""
    logger.info("🔄 Restarter Docusaurus for å laste nye data...")
    
    # Stopp eksisterende prosess
    success, _ = run_command("pkill -f 'docusaurus start --port 3001'", "Stopper Docusaurus")
    
    # Vent litt
    import time
    time.sleep(3)
    
    # Start på nytt
    success, _ = run_command("nohup npm start --port 3001 > logs/docusaurus.log 2>&1 &", "Starter Docusaurus")
    
    if success:
        logger.info("✅ Docusaurus restartet")
    else:
        logger.warning("⚠️ Kunne ikke restarte Docusaurus automatisk")

def cleanup_old_logs():
    """Slett gamle log-filer (eldre enn 30 dager)"""
    log_dir = Path(__file__).parent.parent / "logs"
    if not log_dir.exists():
        return
    
    cutoff_date = datetime.date.today() - datetime.timedelta(days=30)
    
    for log_file in log_dir.glob("protonord_sync_*.log"):
        try:
            # Ekstraher dato fra filnavn
            date_str = log_file.stem.replace("protonord_sync_", "")
            file_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            
            if file_date < cutoff_date:
                log_file.unlink()
                logger.info(f"🗑️ Slettet gammel log: {log_file.name}")
        except Exception as e:
            logger.warning(f"Kunne ikke slette {log_file.name}: {e}")

if __name__ == "__main__":
    try:
        # Cleanup gamle logs
        cleanup_old_logs()
        
        # Kjør synkronisering
        success = sync_protonord_data()
        
        if success:
            # Restart Docusaurus for å laste nye data
            restart_docusaurus()
            logger.info("🎉 Automatisk synkronisering fullført!")
            sys.exit(0)
        else:
            logger.error("💥 Synkronisering feilet")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("⏹️ Synkronisering avbrutt av bruker")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Uventet feil: {e}")
        sys.exit(1)