#!/usr/bin/env python3
"""
Fikser bildestrukturen i MinIO - flytter bilder fra mapper til faktiske filer.
"""

import os
import shutil
from pathlib import Path

def fix_image_structure():
    """Fikser bildestrukturen ved å flytte bilder fra undermapper til faktiske filer."""
    
    minio_products_dir = Path("/mnt/data/products")
    fixed_count = 0
    
    print("🔧 Fikser bildestruktur i MinIO...")
    
    # Finn alle produktmapper
    for product_dir in minio_products_dir.rglob("*/"):
        if not product_dir.is_dir():
            continue
            
        images_dir = product_dir / "images"
        if not images_dir.exists():
            continue
            
        # Sjekk om vi har bildemapper som skal være filer
        needs_fixing = False
        for item in images_dir.iterdir():
            if item.is_dir() and (item.name.endswith('.jpg') or item.name.endswith('.png') or item.name.endswith('.jpeg')):
                needs_fixing = True
                break
        
        if not needs_fixing:
            continue
            
        print(f"🔧 Fikser {product_dir.name}...")
        
        # Flytt bilder fra undermapper til faktiske filer
        for image_folder in images_dir.iterdir():
            if image_folder.is_dir() and (image_folder.name.endswith('.jpg') or image_folder.name.endswith('.png') or image_folder.name.endswith('.jpeg')):
                # Finn den faktiske bildefilen inne i mappen
                actual_image_files = list(image_folder.rglob("*.jpg")) + list(image_folder.rglob("*.png")) + list(image_folder.rglob("*.jpeg"))
                
                if actual_image_files:
                    # Ta den første bildefilen vi finner
                    source_file = actual_image_files[0]
                    target_file = images_dir / image_folder.name
                    
                    try:
                        # Kopier bildet til riktig sted
                        shutil.copy2(source_file, target_file)
                        # Fjern den gamle mappen
                        shutil.rmtree(image_folder)
                        print(f"  ✅ Flyttet {image_folder.name}")
                    except Exception as e:
                        print(f"  ❌ Feil ved {image_folder.name}: {e}")
        
        fixed_count += 1
    
    print(f"\n🎉 Fikset bildestruktur for {fixed_count} produkter")

if __name__ == "__main__":
    fix_image_structure()