import json
import os
from pathlib import Path
from typing import Dict, List
from .config import (
    SHOPIFY_SHOP, SHOPIFY_ACCESS_TOKEN, DATA_ROOT,
    validate
)
from .shopify_client import ShopifyClient

def sync_product_to_shopify(product_dir: Path) -> bool:
    """Sync a single product folder back to Shopify"""
    product_json_path = product_dir / "product.json"
    description_path = product_dir / "description.md"
    
    if not product_json_path.exists():
        print(f"Error: {product_json_path} not found")
        return False
    
    # Load product data
    with open(product_json_path, "r", encoding="utf-8") as f:
        product_data = json.load(f)
    
    # Load description if it exists
    if description_path.exists():
        with open(description_path, "r", encoding="utf-8") as f:
            description_content = f.read()
            # Remove the comment line if it exists
            if description_content.startswith("<!-- Edit this file"):
                lines = description_content.split("\n")
                description_content = "\n".join(lines[2:]).strip()
            product_data["body_html"] = description_content
    
    # Connect to Shopify
    shopify_client = ShopifyClient(SHOPIFY_SHOP, SHOPIFY_ACCESS_TOKEN)
    
    try:
        product_id = product_data.get("id")
        if not product_id:
            print(f"Error: No Shopify ID found in {product_json_path}")
            return False
        
        # Prepare update data (exclude read-only fields)
        update_data = {
            "title": product_data.get("title"),
            "body_html": product_data.get("body_html"),
            "product_type": product_data.get("product_type"),
            "vendor": product_data.get("vendor"),
            "tags": product_data.get("tags"),
            "status": product_data.get("status"),
        }
        
        # Update variants if they exist
        if product_data.get("variants"):
            update_data["variants"] = []
            for variant in product_data["variants"]:
                variant_update = {
                    "id": variant.get("id"),
                    "price": variant.get("price"),
                    "compare_at_price": variant.get("compare_at_price"),
                    "sku": variant.get("sku"),
                    "barcode": variant.get("barcode"),
                    "weight": variant.get("weight"),
                    "weight_unit": variant.get("weight_unit"),
                    "inventory_policy": variant.get("inventory_policy"),
                    "taxable": variant.get("taxable"),
                    "requires_shipping": variant.get("requires_shipping"),
                }
                update_data["variants"].append(variant_update)
        
        # Update product in Shopify
        updated_product = shopify_client.update_product(product_id, update_data)
        print(f"✅ Updated product: {updated_product.get('title')} (ID: {product_id})")
        
        # Update local JSON with any changes from Shopify
        product_data.update({
            "updated_at": updated_product.get("updated_at"),
            "title": updated_product.get("title"),
            "body_html": updated_product.get("body_html"),
        })
        
        with open(product_json_path, "w", encoding="utf-8") as f:
            json.dump(product_data, f, ensure_ascii=False, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Error updating product {product_data.get('title', 'Unknown')}: {e}")
        return False

def sync_all_products() -> None:
    """Sync all products in the catalog to Shopify"""
    print("🔄 Starting sync to Shopify...")
    
    validate()
    
    catalog_path = Path(DATA_ROOT)
    if not catalog_path.exists():
        print(f"Error: Catalog directory {catalog_path} not found")
        return
    
    # Find all product directories (containing product.json)
    product_dirs = []
    for item in catalog_path.iterdir():
        if item.is_dir() and (item / "product.json").exists():
            product_dirs.append(item)
    
    if not product_dirs:
        print("No product directories found")
        return
    
    print(f"Found {len(product_dirs)} products to sync")
    
    successful = 0
    failed = 0
    
    for product_dir in product_dirs:
        print(f"\nSyncing: {product_dir.name}")
        if sync_product_to_shopify(product_dir):
            successful += 1
        else:
            failed += 1
    
    print(f"\n📊 Sync complete:")
    print(f"   ✅ {successful} products updated successfully")
    print(f"   ❌ {failed} products failed to update")

def sync_specific_product(handle: str) -> None:
    """Sync a specific product by handle"""
    validate()
    
    catalog_path = Path(DATA_ROOT)
    product_dir = catalog_path / handle
    
    if not product_dir.exists():
        print(f"Error: Product directory {product_dir} not found")
        return
    
    if not (product_dir / "product.json").exists():
        print(f"Error: product.json not found in {product_dir}")
        return
    
    print(f"🔄 Syncing product: {handle}")
    
    if sync_product_to_shopify(product_dir):
        print(f"✅ Successfully synced {handle}")
    else:
        print(f"❌ Failed to sync {handle}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        handle = sys.argv[1]
        sync_specific_product(handle)
    else:
        sync_all_products()