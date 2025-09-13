import json
import subprocess
from pathlib import Path
from .config import (
    SHOPIFY_SHOP, SHOPIFY_ACCESS_TOKEN, DATA_ROOT,
    validate
)
from .shopify_client import ShopifyClient
from .bootstrap_catalog import normalize_handle, create_product_folder

def create_new_product(
    title: str,
    product_type: str = "",
    vendor: str = "",
    description: str = "",
    status: str = "draft"
) -> str:
    """Create a new product both locally and in Shopify"""
    print(f"🆕 Creating new product: {title}")
    
    validate()
    
    # Generate handle
    handle = normalize_handle(title)
    
    # Setup paths
    catalog_path = Path(DATA_ROOT)
    catalog_path.mkdir(exist_ok=True)
    product_dir = catalog_path / handle
    
    if product_dir.exists():
        print(f"Warning: Product directory {handle} already exists")
        return handle
    
    # Initialize Shopify client
    shopify_client = ShopifyClient(SHOPIFY_SHOP, SHOPIFY_ACCESS_TOKEN)
    
    # Create product in Shopify first
    product_data = {
        "title": title,
        "body_html": description,
        "product_type": product_type,
        "vendor": vendor,
        "status": status,
        "handle": handle,
    }
    
    try:
        created_product = shopify_client.create_product(product_data)
        print(f"✅ Created product in Shopify with ID: {created_product.get('id')}")
        
        # Create local folder structure
        product_info = create_product_folder(catalog_path, created_product)
        
        print(f"📁 Created local structure at: {product_info['directory']}")
        print(f"☁️ Cloud backup path ready: {handle}/")
        
        return handle
        
    except Exception as e:
        print(f"❌ Error creating product: {e}")
        raise

def add_files_to_product(handle: str, files: list) -> None:
    """Add files to a product's cloud storage"""
    validate()
    
    # Setup local product directory
    catalog_path = Path(DATA_ROOT)
    product_dir = catalog_path / handle
    
    if not product_dir.exists():
        print(f"❌ Product directory {handle} not found")
        return
    
    for file_path in files:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"Warning: File {file_path} not found")
            continue
        
        # Determine file category based on extension
        suffix = file_path.suffix.lower()
        if suffix in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            category = 'images'
        elif suffix in ['.step', '.stp', '.stl', '.dwg', '.dxf', '.iges', '.igs']:
            category = 'cad'
        else:
            category = 'documentation'
        
        # Create local category directory
        category_dir = product_dir / category
        category_dir.mkdir(exist_ok=True)
        
        # Copy file to local structure
        destination = category_dir / file_path.name
        try:
            import shutil
            shutil.copy2(file_path, destination)
            print(f"📎 Added {file_path.name} to {category}/")
            
            # Sync to cloud backup
            cloud_path = f"catalog/{handle}/{category}/"
            try:
                # Sync to Google Drive
                result = subprocess.run([
                    "rclone", "copy", str(destination), f"gdrive:backup/{cloud_path}"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"☁️ Synced {file_path.name} to Google Drive")
                else:
                    print(f"⚠️ Google Drive sync warning: {result.stderr}")
                
                # Sync to Jottacloud as backup
                result = subprocess.run([
                    "rclone", "copy", str(destination), f"jottacloud:backup/{cloud_path}"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"☁️ Synced {file_path.name} to Jottacloud backup")
                else:
                    print(f"⚠️ Jottacloud sync warning: {result.stderr}")
                    
            except Exception as e:
                print(f"⚠️ Cloud sync error for {file_path.name}: {e}")
                
        except Exception as e:
            print(f"❌ Failed to add {file_path.name}: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m src.new_product <title> [product_type] [vendor] [description]")
        sys.exit(1)
    
    title = sys.argv[1]
    product_type = sys.argv[2] if len(sys.argv) > 2 else ""
    vendor = sys.argv[3] if len(sys.argv) > 3 else ""
    description = sys.argv[4] if len(sys.argv) > 4 else ""
    
    handle = create_new_product(title, product_type, vendor, description)
    print(f"\n🎉 Product '{title}' created successfully!")
    print(f"   Handle: {handle}")
    print(f"   Edit files in: catalog/{handle}/")
    print(f"   Upload assets to: catalog/{handle}/images/ or catalog/{handle}/cad/")
    print(f"   Sync changes: python -m src.sync_to_shopify {handle}")
    print(f"   Backup to cloud: bash scripts/protonord_cloud_backup.sh")