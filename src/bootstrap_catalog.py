import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from slugify import slugify

from .config import (
    SHOPIFY_SHOP, SHOPIFY_ACCESS_TOKEN, DATA_ROOT,
    MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET, MINIO_SECURE,
    validate
)
from .shopify_client import ShopifyClient
from .minio_client import create_minio_client, ensure_bucket_exists, upload_bytes_to_minio
import requests

def normalize_handle(text: str) -> str:
    """Convert text to a normalized handle suitable for folders and URLs"""
    if not text:
        return "product"
    
    # Use slugify for basic normalization
    handle = slugify(text, separator="-")
    
    # Additional cleanup for consistency
    handle = re.sub(r"[^a-z0-9-]", "", handle.lower())
    handle = re.sub(r"-+", "-", handle)  # Remove multiple consecutive dashes
    handle = handle.strip("-")  # Remove leading/trailing dashes
    
    return handle or "product"

def create_product_folder(root_path: Path, product: Dict) -> Dict:
    """Create local folder structure for a product"""
    handle = product.get("handle") or normalize_handle(product.get("title", "product"))
    product_dir = root_path / handle
    
    # Create directories
    product_dir.mkdir(parents=True, exist_ok=True)
    (product_dir / "images").mkdir(exist_ok=True)
    (product_dir / "cad").mkdir(exist_ok=True)
    (product_dir / "documentation").mkdir(exist_ok=True)
    
    # Create product.json with essential data
    product_data = {
        "id": product.get("id"),
        "title": product.get("title"),
        "handle": handle,
        "status": product.get("status"),
        "product_type": product.get("product_type"),
        "vendor": product.get("vendor"),
        "tags": product.get("tags", ""),
        "options": product.get("options", []),
        "variants": [
            {
                "id": variant.get("id"),
                "title": variant.get("title"),
                "sku": variant.get("sku"),
                "price": variant.get("price"),
                "compare_at_price": variant.get("compare_at_price"),
                "barcode": variant.get("barcode"),
                "weight": variant.get("weight"),
                "weight_unit": variant.get("weight_unit"),
                "inventory_policy": variant.get("inventory_policy"),
                "taxable": variant.get("taxable"),
                "requires_shipping": variant.get("requires_shipping"),
            }
            for variant in (product.get("variants") or [])
        ],
        "body_html": product.get("body_html") or "",
        "image_count": len(product.get("images") or []),
        "created_at": product.get("created_at"),
        "updated_at": product.get("updated_at"),
    }
    
    # Write product.json
    with open(product_dir / "product.json", "w", encoding="utf-8") as f:
        json.dump(product_data, f, ensure_ascii=False, indent=2)
    
    # Create editable description.md
    body_html = product.get("body_html") or ""
    with open(product_dir / "description.md", "w", encoding="utf-8") as f:
        f.write("<!-- Edit this file to change the product description -->\n\n")
        f.write(body_html)
    
    # Create README.md for the product
    with open(product_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(f"# {product.get('title', 'Product')}\n\n")
        f.write(f"**Handle:** `{handle}`  \n")
        f.write(f"**Status:** {product.get('status', 'draft')}  \n")
        f.write(f"**Type:** {product.get('product_type', 'N/A')}  \n")
        f.write(f"**Vendor:** {product.get('vendor', 'N/A')}  \n")
        f.write(f"**Shopify ID:** {product.get('id')}  \n\n")
        
        f.write("## Folder Structure\n\n")
        f.write("- `product.json` - Product data synchronized with Shopify\n")
        f.write("- `description.md` - Editable product description (HTML)\n")
        f.write("- `images/` - Product images (stored in MinIO)\n")
        f.write("- `cad/` - CAD files and technical drawings (stored in MinIO)\n")
        f.write("- `documentation/` - Additional documentation and notes\n\n")
        
        f.write("## Editing\n\n")
        f.write("1. Edit `product.json` or `description.md` to change product info\n")
        f.write("2. Upload files to MinIO using the web interface or CLI\n")
        f.write("3. Run sync script to push changes back to Shopify\n\n")
        
        if product.get("variants"):
            f.write("## Variants\n\n")
            for variant in product.get("variants", []):
                f.write(f"- **{variant.get('title')}**")
                if variant.get("sku"):
                    f.write(f" (SKU: {variant.get('sku')})")
                if variant.get("price"):
                    f.write(f" - ${variant.get('price')}")
                f.write("\n")
    
    return {
        "directory": str(product_dir),
        "handle": handle,
        "product_id": product.get("id")
    }

def download_and_store_images(images: List[Dict], handle: str, minio_client, bucket: str) -> None:
    """Download product images and store them in MinIO"""
    for index, image in enumerate(images or []):
        image_url = image.get("src")
        if not image_url:
            continue
            
        try:
            # Download image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Determine file extension from content type
            content_type = response.headers.get("Content-Type", "")
            extension = "jpg"  # default
            if "png" in content_type:
                extension = "png"
            elif "webp" in content_type:
                extension = "webp"
            elif "gif" in content_type:
                extension = "gif"
            
            # Create object name
            object_name = f"{handle}/images/{index + 1}.{extension}"
            
            # Upload to MinIO
            upload_bytes_to_minio(
                minio_client, 
                bucket, 
                object_name, 
                response.content, 
                content_type or "application/octet-stream"
            )
            
        except Exception as e:
            print(f"Warning: Failed to download/store image {image_url}: {e}")

def bootstrap_from_shopify():
    """Main function to bootstrap catalog from Shopify"""
    print("🚀 Starting Shopify catalog bootstrap...")
    
    # Validate configuration
    validate()
    
    # Setup paths
    catalog_path = Path(DATA_ROOT)
    catalog_path.mkdir(exist_ok=True)
    
    # Initialize clients
    print("📡 Connecting to Shopify...")
    shopify_client = ShopifyClient(SHOPIFY_SHOP, SHOPIFY_ACCESS_TOKEN)
    
    print("🗄️ Connecting to MinIO...")
    minio_client = create_minio_client(
        MINIO_ENDPOINT, 
        MINIO_ACCESS_KEY, 
        MINIO_SECRET_KEY, 
        MINIO_SECURE
    )
    ensure_bucket_exists(minio_client, MINIO_BUCKET)
    
    # Fetch products from Shopify
    print("📦 Fetching products from Shopify...")
    products = shopify_client.list_products()
    print(f"Found {len(products)} products")
    
    # Process each product
    print("📁 Creating local catalog structure...")
    created_products = []
    
    for i, product in enumerate(products, 1):
        print(f"Processing product {i}/{len(products)}: {product.get('title', 'Unknown')}")
        
        # Create local folder structure
        product_info = create_product_folder(catalog_path, product)
        created_products.append(product_info)
        
        # Download and store images in MinIO
        if product.get("images"):
            print(f"  └─ Storing {len(product['images'])} images in MinIO...")
            download_and_store_images(
                product["images"], 
                product_info["handle"], 
                minio_client, 
                MINIO_BUCKET
            )
    
    # Create summary
    print("\n📊 Creating catalog summary...")
    summary = {
        "total_products": len(created_products),
        "catalog_path": str(catalog_path.resolve()),
        "minio_bucket": MINIO_BUCKET,
        "products": [
            {
                "handle": p["handle"],
                "directory": p["directory"],
                "shopify_id": p["product_id"]
            }
            for p in created_products
        ]
    }
    
    with open(catalog_path / "catalog_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Bootstrap complete!")
    print(f"   📁 Catalog created in: {catalog_path.resolve()}")
    print(f"   📦 {len(created_products)} products processed")
    print(f"   🗄️ Images stored in MinIO bucket: {MINIO_BUCKET}")
    print(f"\n🔄 Next steps:")
    print(f"   1. Review the created folder structure")
    print(f"   2. Commit and push to GitHub: git add catalog && git commit -m 'Bootstrap catalog from Shopify' && git push")
    print(f"   3. Edit product.json files to make changes")
    print(f"   4. Use sync scripts to push changes back to Shopify")

if __name__ == "__main__":
    bootstrap_from_shopify()