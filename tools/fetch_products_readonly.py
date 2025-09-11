#!/usr/bin/env python3
"""
Read-only Shopify product fetcher
Safely fetch and explore products without any write operations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.shopify_client import ShopifyClient
import json
from datetime import datetime

def fetch_products_readonly(shop_domain, access_token, limit=10):
    """
    Safely fetch products from Shopify (read-only)
    
    Args:
        shop_domain: Your Shopify store (e.g., "yourstore.myshopify.com")
        access_token: Admin API access token
        limit: Number of products to fetch (default 10)
    """
    print(f"🔍 Fetching {limit} products from {shop_domain}...")
    print("📖 READ-ONLY MODE - No changes will be made to your store")
    print("-" * 60)
    
    try:
        # Initialize client
        client = ShopifyClient(shop_domain, access_token)
        
        # Test connection first
        response = client.session.get(f"{client.base_url}/shop.json")
        if response.status_code != 200:
            print(f"❌ Connection failed: HTTP {response.status_code}")
            return
        
        shop_info = response.json().get('shop', {})
        print(f"✅ Connected to: {shop_info.get('name', 'Unknown Shop')}")
        print(f"   Domain: {shop_info.get('domain', 'Unknown')}")
        print(f"   Currency: {shop_info.get('currency', 'Unknown')}")
        print("")
        
        # Fetch products
        products = client.list_products(limit=limit)
        
        if not products:
            print("📭 No products found in your store")
            return
        
        print(f"📦 Found {len(products)} products:")
        print("=" * 60)
        
        for i, product in enumerate(products, 1):
            print(f"\n{i}. {product.get('title', 'Untitled Product')}")
            print(f"   ID: {product.get('id')}")
            print(f"   Handle: {product.get('handle', 'no-handle')}")
            print(f"   Status: {product.get('status', 'unknown')}")
            print(f"   Type: {product.get('product_type', 'No type')}")
            print(f"   Vendor: {product.get('vendor', 'No vendor')}")
            print(f"   Variants: {len(product.get('variants', []))}")
            print(f"   Images: {len(product.get('images', []))}")
            
            # Show first variant info if exists
            variants = product.get('variants', [])
            if variants:
                first_variant = variants[0]
                price = first_variant.get('price', 'N/A')
                sku = first_variant.get('sku', 'No SKU')
                print(f"   Price: ${price} (SKU: {sku})")
            
            # Show tags if any
            tags = product.get('tags', '')
            if tags:
                print(f"   Tags: {tags}")
        
        # Save to file for inspection
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"shopify_products_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Full product data saved to: {filename}")
        print(f"   You can inspect this file to see all available product fields")
        
        print(f"\n📊 Summary:")
        print(f"   Total products fetched: {len(products)}")
        
        # Count by status
        statuses = {}
        for product in products:
            status = product.get('status', 'unknown')
            statuses[status] = statuses.get(status, 0) + 1
        
        for status, count in statuses.items():
            print(f"   {status.title()}: {count}")
        
        print(f"\n✅ Read-only fetch completed successfully!")
        print(f"   No changes were made to your Shopify store")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\nTroubleshooting:")
        print(f"1. Check shop domain format: 'yourstore.myshopify.com'")
        print(f"2. Verify access token starts with 'shpat_'")
        print(f"3. Ensure Custom App has 'read_products' permission")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Safely fetch Shopify products (read-only)")
    parser.add_argument("--shop", required=True, help="Shopify store domain (yourstore.myshopify.com)")
    parser.add_argument("--token", required=True, help="Admin API access token")
    parser.add_argument("--limit", type=int, default=10, help="Number of products to fetch (default: 10)")
    parser.add_argument("--all", action="store_true", help="Fetch ALL products (use with caution)")
    
    args = parser.parse_args()
    
    if args.all:
        print("⚠️ Fetching ALL products from your store...")
        confirm = input("Are you sure? This might take a while for large stores (y/N): ")
        if confirm.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)
        limit = 1000  # Large number to get all
    else:
        limit = args.limit
    
    fetch_products_readonly(args.shop, args.token, limit)