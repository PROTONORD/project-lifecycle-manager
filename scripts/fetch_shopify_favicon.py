#!/usr/bin/env python3
"""
Script to fetch favicon/logo from Shopify store and save it for Docusaurus.
"""

import os
import sys
import requests
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from shopify_client import ShopifyClient

def download_favicon_from_shopify():
    """Download favicon from Shopify store"""
    
    # Get credentials from environment
    shop = os.getenv('SHOPIFY_SHOP', 'protonord')
    token = os.getenv('SHOPIFY_ACCESS_TOKEN')
    
    if not token:
        print("❌ SHOPIFY_ACCESS_TOKEN environment variable not set")
        return False
    
    try:
        # Initialize Shopify client
        client = ShopifyClient(shop, token)
        
        # Get shop information
        print("📡 Fetching shop information...")
        shop_info = client.get_shop_info()
        
        # Check if shop has a logo
        if 'logo' in shop_info:
            logo_url = shop_info['logo']
            print(f"🎯 Found shop logo: {logo_url}")
            
            # Download logo
            response = requests.get(logo_url)
            response.raise_for_status()
            
            # Save as favicon.ico
            static_img_path = Path(__file__).parent.parent / "static" / "img"
            static_img_path.mkdir(parents=True, exist_ok=True)
            
            favicon_path = static_img_path / "favicon.ico"
            
            # Backup existing favicon
            if favicon_path.exists():
                backup_path = static_img_path / "favicon_backup.ico"
                favicon_path.rename(backup_path)
                print(f"📦 Backed up existing favicon to {backup_path}")
            
            # Save new favicon
            with open(favicon_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Successfully downloaded favicon to {favicon_path}")
            return True
        
        # Try to get themes and look for favicon/logo assets
        print("🎨 Checking themes for logo assets...")
        themes = client.get_themes()
        
        for theme in themes:
            if theme.get('role') == 'main':  # Current active theme
                theme_id = theme['id']
                print(f"🎯 Found main theme: {theme['name']} (ID: {theme_id})")
                
                # Get theme assets
                assets = client.get_theme_assets(theme_id)
                
                # Look for common favicon/logo files
                favicon_assets = []
                for asset in assets.get('assets', []):
                    asset_key = asset.get('key', '')
                    # Look for actual image files, not liquid templates
                    if (any(term in asset_key.lower() for term in ['favicon', 'logo', 'icon']) and 
                        any(ext in asset_key.lower() for ext in ['.ico', '.png', '.jpg', '.jpeg', '.svg', '.gif']) and
                        '.liquid' not in asset_key.lower()):
                        favicon_assets.append(asset)
                
                if favicon_assets:
                    print(f"🎯 Found {len(favicon_assets)} potential favicon/logo assets:")
                    for asset in favicon_assets:
                        print(f"  - {asset.get('key')}")
                    
                    # Try to download the first favicon asset
                    first_asset = favicon_assets[0]
                    asset_key = first_asset.get('key')
                    
                    # Get the actual asset content
                    asset_content = client.get_theme_assets(theme_id, asset_key)
                    
                    if 'attachment' in asset_content.get('asset', {}):
                        # Asset is binary (image)
                        import base64
                        attachment = asset_content['asset']['attachment']
                        content = base64.b64decode(attachment)
                        
                        static_img_path = Path(__file__).parent.parent / "static" / "img"
                        static_img_path.mkdir(parents=True, exist_ok=True)
                        
                        favicon_path = static_img_path / "favicon.ico"
                        
                        # Backup existing favicon
                        if favicon_path.exists():
                            backup_path = static_img_path / "favicon_backup.ico"
                            favicon_path.rename(backup_path)
                            print(f"📦 Backed up existing favicon to {backup_path}")
                        
                        # Save new favicon
                        with open(favicon_path, 'wb') as f:
                            f.write(content)
                        
                        print(f"✅ Successfully downloaded favicon from theme asset: {asset_key}")
                        return True
                
                break
        
        print("❌ No favicon or logo found in Shopify store")
        return False
        
    except Exception as e:
        print(f"❌ Error fetching favicon from Shopify: {e}")
        return False

if __name__ == "__main__":
    print("🛍️ Fetching favicon from Shopify store...")
    
    if download_favicon_from_shopify():
        print("🎉 Favicon successfully updated!")
    else:
        print("❌ Failed to fetch favicon from Shopify")
        sys.exit(1)