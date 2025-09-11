import json
from pathlib import Path
from .config import (
    SHOPIFY_SHOP, SHOPIFY_ACCESS_TOKEN, DATA_ROOT,
    MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET, MINIO_SECURE,
    validate
)
from .shopify_client import ShopifyClient
from .minio_client import create_minio_client, ensure_bucket_exists, upload_file_to_minio
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
    
    # Initialize clients
    shopify_client = ShopifyClient(SHOPIFY_SHOP, SHOPIFY_ACCESS_TOKEN)
    minio_client = create_minio_client(
        MINIO_ENDPOINT, 
        MINIO_ACCESS_KEY, 
        MINIO_SECRET_KEY, 
        MINIO_SECURE
    )
    ensure_bucket_exists(minio_client, MINIO_BUCKET)
    
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
        print(f"🗄️ MinIO path ready: {MINIO_BUCKET}/{handle}/")
        
        return handle
        
    except Exception as e:
        print(f"❌ Error creating product: {e}")
        raise

def add_files_to_product(handle: str, files: list) -> None:
    """Add files to a product's MinIO storage"""
    validate()
    
    minio_client = create_minio_client(
        MINIO_ENDPOINT, 
        MINIO_ACCESS_KEY, 
        MINIO_SECRET_KEY, 
        MINIO_SECURE
    )
    
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
        
        # Upload to MinIO
        object_name = f"{handle}/{category}/{file_path.name}"
        
        try:
            upload_file_to_minio(
                minio_client,
                MINIO_BUCKET,
                object_name,
                str(file_path)
            )
            print(f"📎 Uploaded {file_path.name} to {category}/")
        except Exception as e:
            print(f"❌ Failed to upload {file_path.name}: {e}")

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
    print(f"   Upload assets to MinIO bucket: {MINIO_BUCKET}/{handle}/")
    print(f"   Sync changes: python -m src.sync_to_shopify {handle}")