#!/usr/bin/env python3
"""
Test Shopify API connection and permissions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import validate, SHOPIFY_SHOP, SHOPIFY_ACCESS_TOKEN
from src.shopify_client import ShopifyClient

def test_shopify_connection():
    """Test Shopify API connection and required permissions"""
    print("🔍 Testing Shopify API connection...")
    
    try:
        validate()
        print("✅ Environment variables loaded successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    try:
        client = ShopifyClient(SHOPIFY_SHOP, SHOPIFY_ACCESS_TOKEN)
        
        # Test basic connection by getting shop info
        response = client.session.get(f"{client.base_url}/shop.json")
        if response.status_code == 200:
            shop_data = response.json().get("shop", {})
            print(f"✅ Connected to shop: {shop_data.get('name', 'Unknown')}")
            print(f"   Domain: {shop_data.get('domain', 'Unknown')}")
        else:
            print(f"❌ Failed to connect: HTTP {response.status_code}")
            return False
        
        # Test product access
        print("\n🛍️ Testing product access...")
        products = client.list_products(limit=5)
        print(f"✅ Successfully fetched {len(products)} sample products")
        
        if products:
            first_product = products[0]
            print(f"   Sample product: {first_product.get('title', 'Unknown')}")
        
        # Test required scopes
        print("\n🔐 Testing API scopes...")
        
        # Test products scope
        response = client.session.get(f"{client.base_url}/products.json?limit=1")
        if response.status_code == 200:
            print("✅ Products scope: OK")
        else:
            print(f"❌ Products scope: Failed (HTTP {response.status_code})")
        
        # Test files scope (if available)
        response = client.session.get(f"{client.base_url}/themes.json?limit=1")
        if response.status_code == 200:
            print("✅ Files/Themes scope: OK")
        elif response.status_code == 403:
            print("⚠️ Files scope: Limited (may need additional permissions)")
        else:
            print(f"❌ Files scope: Failed (HTTP {response.status_code})")
        
        print("\n✅ Shopify connection test completed successfully!")
        print("\nNext steps:")
        print("1. Run: python main.py bootstrap")
        print("2. Review created catalog structure")
        print("3. Test sync: python main.py sync --dry-run")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Verify SHOPIFY_SHOP format (yourstore.myshopify.com)")
        print("2. Check SHOPIFY_ACCESS_TOKEN is correct")
        print("3. Ensure Custom App has required permissions")
        print("4. Check network connectivity")
        return False

if __name__ == "__main__":
    success = test_shopify_connection()
    sys.exit(0 if success else 1)