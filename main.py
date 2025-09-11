#!/usr/bin/env python3
"""
Shopify-MinIO-GitHub Integration CLI

Main command-line interface for managing the product catalog workflow.
"""

import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Shopify-MinIO-GitHub Product Catalog Management",
        epilog="Examples:\n"
               "  %(prog)s bootstrap    # Import all products from Shopify\n"
               "  %(prog)s sync         # Sync all local changes to Shopify\n"
               "  %(prog)s sync product-handle  # Sync specific product\n"
               "  %(prog)s new \"My Product\" \"Electronics\" \"ACME Corp\"  # Create new product\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Bootstrap command
    bootstrap_parser = subparsers.add_parser(
        'bootstrap', 
        help='Import all products from Shopify to create local catalog'
    )
    
    # Sync command
    sync_parser = subparsers.add_parser(
        'sync',
        help='Sync local changes back to Shopify'
    )
    sync_parser.add_argument(
        'handle',
        nargs='?',
        help='Product handle to sync (optional, syncs all if not specified)'
    )
    sync_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test sync without making actual changes'
    )
    
    # New product command
    new_parser = subparsers.add_parser(
        'new',
        help='Create a new product'
    )
    new_parser.add_argument('title', help='Product title')
    new_parser.add_argument('--type', dest='product_type', default='', help='Product type')
    new_parser.add_argument('--vendor', default='', help='Vendor/brand name')
    new_parser.add_argument('--description', default='', help='Product description')
    new_parser.add_argument('--status', default='draft', choices=['draft', 'active'], help='Product status')
    
    # Status command
    status_parser = subparsers.add_parser(
        'status',
        help='Show catalog status'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'bootstrap':
            from src.bootstrap_catalog import bootstrap_from_shopify
            bootstrap_from_shopify()
            
        elif args.command == 'sync':
            if args.handle:
                from src.sync_to_shopify import sync_specific_product
                sync_specific_product(args.handle, args.dry_run)
            else:
                from src.sync_to_shopify import sync_all_products
                sync_all_products(args.dry_run)
                
        elif args.command == 'new':
            from src.new_product import create_new_product
            handle = create_new_product(
                args.title,
                args.product_type,
                args.vendor,
                args.description,
                args.status
            )
            print(f"\n✨ Next steps:")
            print(f"   1. Edit product details: catalog/{handle}/product.json")
            print(f"   2. Upload files to MinIO bucket")
            print(f"   3. Sync to Shopify: python main.py sync {handle}")
            
        elif args.command == 'status':
            show_status()
            
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def show_status():
    """Show current catalog status"""
    from src.config import DATA_ROOT, MINIO_BUCKET
    import json
    
    catalog_path = Path(DATA_ROOT)
    
    print("📊 Catalog Status")
    print("=" * 50)
    
    if not catalog_path.exists():
        print("❌ Catalog directory not found. Run 'bootstrap' first.")
        return
    
    # Count products
    product_dirs = [d for d in catalog_path.iterdir() 
                   if d.is_dir() and (d / "product.json").exists()]
    
    print(f"📁 Catalog path: {catalog_path.resolve()}")
    print(f"📦 Products found: {len(product_dirs)}")
    print(f"🗄️ MinIO bucket: {MINIO_BUCKET}")
    
    if product_dirs:
        print("\n📋 Products:")
        for product_dir in sorted(product_dirs):
            try:
                with open(product_dir / "product.json") as f:
                    data = json.load(f)
                status = data.get("status", "unknown")
                title = data.get("title", "Unknown")
                print(f"   {product_dir.name} - {title} ({status})")
            except:
                print(f"   {product_dir.name} - (error reading product.json)")
    
    # Check for summary file
    summary_file = catalog_path / "catalog_summary.json"
    if summary_file.exists():
        print(f"\n📄 Summary file: {summary_file}")
    
    print(f"\n🔄 Commands:")
    print(f"   Sync all: python main.py sync")
    print(f"   Sync one: python main.py sync <handle>")
    print(f"   New product: python main.py new \"Product Name\"")

if __name__ == "__main__":
    main()