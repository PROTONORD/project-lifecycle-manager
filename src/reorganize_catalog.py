#!/usr/bin/env python3
"""
Reorganize catalog structure by Shopify categories
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List
import argparse
from slugify import slugify

def normalize_category(product_type: str) -> str:
    """Normalize product type to a clean folder name"""
    category_map = {
        "Tilbehør til kjøretøy": "tilbehor-til-kjoretoy",
        "Diverse": "diverse", 
        "Smarthus": "smarthus",
        "Kamerautstyr": "kamerautstyr",
        "Netatmo": "smarthus",  # Merge Netatmo into Smarthus
        "Verktøy og Oppbevaring": "verktoy-og-oppbevaring",
        "Tilbehør til Robotklipper": "hage-og-utendors",
        "sykkel": "sport-og-fritid"
    }
    
    return category_map.get(product_type, slugify(product_type) if product_type else "ukategorisert")

def get_subcategory(product: Dict, product_type: str) -> str:
    """Determine subcategory based on product type and tags"""
    tags = product.get('tags', '').lower()
    title = product.get('title', '').lower()
    
    if product_type == "Tilbehør til kjøretøy":
        if any(tag in tags for tag in ['chargercover', 'ladeportdeksel', 'værdeksel', 'snødeksel']):
            return "ladeportdeksler"
        elif any(word in title for word in ['koppholder', 'holder', 'brakett']):
            return "interiortilbehor"
        elif any(word in title for word in ['skvettlapper', 'hengerfeste']):
            return "eksteriortilbehor"
        else:
            return "diverse-tilbehor"
    
    elif product_type in ["Smarthus", "Netatmo"]:
        if any(word in tags for word in ['sensor', 'temperatur', 'fuktighet']):
            return "sensorer"
        elif any(word in tags for word in ['styring', 'kontroll', 'switch']):
            return "kontrollere"
        else:
            return "tilbehor"
    
    elif product_type == "Kamerautstyr":
        if any(word in title for word in ['grip', 'håndtak']):
            return "grips-og-handtak"
        elif any(word in title for word in ['deksel', 'cover']):
            return "beskyttelse"
        else:
            return "diverse"
    
    return "diverse"

def reorganize_catalog(catalog_path: Path, dry_run: bool = True):
    """Reorganize catalog into hierarchical structure"""
    
    print(f"🔄 Reorganiserer katalog: {catalog_path}")
    print(f"{'🔍 DRY RUN MODE' if dry_run else '✨ LIVE MODE'}")
    print("=" * 50)
    
    # Create new structure tracking
    new_structure = {}
    moves = []
    
    # Analyze all products
    for product_dir in catalog_path.glob('*/'):
        if not product_dir.is_dir():
            continue
            
        product_file = product_dir / 'product.json'
        if not product_file.exists():
            continue
            
        # Read product data
        with open(product_file) as f:
            product = json.load(f)
        
        product_type = product.get('product_type', '')
        category = normalize_category(product_type)
        subcategory = get_subcategory(product, product_type)
        
        # Create path
        new_path = catalog_path / category / subcategory / product_dir.name
        
        # Track structure
        if category not in new_structure:
            new_structure[category] = {}
        if subcategory not in new_structure[category]:
            new_structure[category][subcategory] = []
        
        new_structure[category][subcategory].append({
            'old_path': product_dir,
            'new_path': new_path,
            'title': product.get('title', 'Unknown'),
            'product_type': product_type
        })
        
        moves.append((product_dir, new_path))
    
    # Print planned structure
    print("📁 Planlagt ny struktur:")
    print("-" * 30)
    total_products = 0
    
    for category, subcats in new_structure.items():
        subcat_count = sum(len(products) for products in subcats.values())
        total_products += subcat_count
        print(f"📂 {category}/ ({subcat_count} produkter)")
        
        for subcat, products in subcats.items():
            print(f"  📁 {subcat}/ ({len(products)} produkter)")
            if len(products) <= 3:  # Show examples for small categories
                for product in products:
                    print(f"    • {product['title'][:50]}...")
            else:  # Show first few examples for large categories
                for product in products[:2]:
                    print(f"    • {product['title'][:50]}...")
                print(f"    • ... og {len(products)-2} flere")
        print()
    
    print(f"📊 Total: {total_products} produkter")
    
    if not dry_run:
        print("\n🚀 Utfører reorganisering...")
        
        # Create directories and move files
        for old_path, new_path in moves:
            new_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"📦 Flytter: {old_path.name} -> {new_path.relative_to(catalog_path)}")
            shutil.move(str(old_path), str(new_path))
        
        print("✅ Reorganisering fullført!")
        
        # Update catalog summary
        summary_file = catalog_path / 'catalog_summary.json'
        if summary_file.exists():
            with open(summary_file) as f:
                summary = json.load(f)
            
            summary['structure'] = 'hierarchical'
            summary['categories'] = {
                cat: {
                    subcat: len(products) 
                    for subcat, products in subcats.items()
                }
                for cat, subcats in new_structure.items()
            }
            
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
    
    else:
        print("\n💡 For å utføre reorganiseringen, kjør:")
        print("   python src/reorganize_catalog.py --execute")

def main():
    parser = argparse.ArgumentParser(description='Reorganize catalog by categories')
    parser.add_argument('--execute', action='store_true', 
                       help='Actually perform the reorganization (default is dry-run)')
    parser.add_argument('--catalog', default='catalog',
                       help='Path to catalog directory')
    
    args = parser.parse_args()
    
    catalog_path = Path(args.catalog)
    if not catalog_path.exists():
        print(f"❌ Katalog ikke funnet: {catalog_path}")
        return 1
    
    reorganize_catalog(catalog_path, dry_run=not args.execute)
    return 0

if __name__ == "__main__":
    exit(main())