#!/usr/bin/env python3
"""
Script to reorganize products in MinIO based on primary Shopify collection
Uses the most relevant collection (excluding system collections)
"""
import sys
import os
from pathlib import Path
import json

# Add src to path
sys.path.append('src')

from dotenv import load_dotenv
from shopify_client import ShopifyClient

load_dotenv()

def get_primary_collection_mapping(shopify_client: ShopifyClient):
    """Get mapping of product handle to primary collection handle"""
    print("Fetching collections and products...")
    
    collections = shopify_client.get_collections()
    products = shopify_client.list_products()
    
    # Filter out system collections
    system_collections = {
        'bestselgere', 'nyeste-produkter', 'orderlyemails-recommended-products', 
        'globofilter-best-selling-products-index'
    }
    
    category_collections = [c for c in collections if c['handle'] not in system_collections]
    
    print(f"Found {len(category_collections)} category collections")
    
    # Create mapping
    product_id_to_handle = {str(product['id']): product['handle'] for product in products}
    product_to_primary_collection = {}
    
    # Priority order for collections (main categories first)
    priority_categories = [
        'audi', 'bmw', 'tesla', 'volkswagen', 'volvo', 'mercedes', 'toyota', 'hyundai', 'kia',
        'ford', 'nissan', 'byd-build-your-dreams', 'fisker-ocean', 'polestar',
        'tilbehor-til-kjoretoy', 'tilbehor-til-kjoretoy-1', 'vaer-og-snodeksler-til-elbiler',
        'biltilbehor', 'fotoutstyr', 'smarthus', 'hus', 'diverse'
    ]
    
    for collection in category_collections:
        collection_handle = collection['handle']
        print(f"Processing: {collection['title']} ({collection_handle})")
        
        try:
            collection_products = shopify_client.get_collection_products(collection['id'])
            for product in collection_products:
                product_handle = product_id_to_handle.get(str(product['id']))
                if product_handle:
                    # Only assign if not already assigned, or if this is a higher priority category
                    if (product_handle not in product_to_primary_collection or 
                        collection_handle in priority_categories):
                        product_to_primary_collection[product_handle] = collection_handle
        except Exception as e:
            print(f"Warning: Error processing {collection_handle}: {e}")
    
    return product_to_primary_collection, {c['handle']: c['title'] for c in category_collections}

def create_reorganization_script(product_mapping, collection_titles):
    """Create bash script to reorganize MinIO structure"""
    
    script_content = """#!/bin/bash
# Auto-generated script to reorganize MinIO products by collection
# Run with: bash reorganize_minio.sh

echo "=== MinIO Reorganization Script ==="
echo "This will move products from flat structure to collection-based structure"
echo "Structure: /collections/{collection}/{product}/"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted"
    exit 1
fi

echo "Starting reorganization..."

"""
    
    # Group products by collection
    collections_products = {}
    for product_handle, collection_handle in product_mapping.items():
        if collection_handle not in collections_products:
            collections_products[collection_handle] = []
        collections_products[collection_handle].append(product_handle)
    
    # Generate move commands for each collection
    for collection_handle, products in collections_products.items():
        collection_title = collection_titles.get(collection_handle, collection_handle)
        script_content += f"""
# === {collection_title} ({collection_handle}) ===
echo "Moving {len(products)} products to {collection_title}..."

"""
        
        for product_handle in products:
            script_content += f"""
# Move {product_handle}
echo "Moving {product_handle}..."
mc mirror localminio/products/{product_handle}/ localminio/products/collections/{collection_handle}/{product_handle}/
if [ $? -eq 0 ]; then
    mc rm --recursive localminio/products/{product_handle}/
    echo "  ✓ Moved {product_handle}"
else
    echo "  ✗ Failed to move {product_handle}"
fi

"""
    
    script_content += """
echo ""
echo "=== Reorganization Complete ==="
echo "New structure: /collections/{collection}/{product}/"
echo ""
echo "Verification:"
mc ls localminio/products/collections/ | head -10
echo ""
echo "You can now access products at: http://172.19.228.199:9001/browser/products/collections/"
"""
    
    return script_content

def main():
    print("=== Shopify Collection-based Reorganization Plan ===")
    
    # Initialize Shopify client
    shop = os.getenv('SHOPIFY_SHOP')
    token = os.getenv('SHOPIFY_ACCESS_TOKEN')
    shopify_client = ShopifyClient(shop, token)
    
    # Get product mapping
    product_mapping, collection_titles = get_primary_collection_mapping(shopify_client)
    
    print(f"\\nFound {len(product_mapping)} products with category assignments")
    
    # Show collection summary
    collection_counts = {}
    for product_handle, collection_handle in product_mapping.items():
        if collection_handle not in collection_counts:
            collection_counts[collection_handle] = 0
        collection_counts[collection_handle] += 1
    
    print("\\nProducts per collection:")
    for collection_handle, count in sorted(collection_counts.items(), key=lambda x: x[1], reverse=True):
        title = collection_titles.get(collection_handle, collection_handle)
        print(f"  {title} ({collection_handle}): {count} products")
    
    # Save mapping as JSON for reference
    mapping_data = {
        'product_to_collection': product_mapping,
        'collection_titles': collection_titles,
        'collection_counts': collection_counts,
        'total_products': len(product_mapping)
    }
    
    with open('product_collection_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping_data, f, indent=2, ensure_ascii=False)
    
    print(f"\\nSaved mapping to: product_collection_mapping.json")
    
    # Generate reorganization script
    script_content = create_reorganization_script(product_mapping, collection_titles)
    
    with open('reorganize_minio.sh', 'w') as f:
        f.write(script_content)
    
    os.chmod('reorganize_minio.sh', 0o755)
    
    print("Generated reorganization script: reorganize_minio.sh")
    print("\\nTo reorganize MinIO:")
    print("  bash reorganize_minio.sh")
    
    print("\\nSample structure after reorganization:")
    for i, (product, collection) in enumerate(list(product_mapping.items())[:5]):
        title = collection_titles.get(collection, collection)
        print(f"  /collections/{collection}/{product}/ ({title})")

if __name__ == "__main__":
    main()