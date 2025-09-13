#!/usr/bin/env python3
"""
Script to extract favicon/logo from Shopify store's public frontend.
"""

import requests
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

def extract_favicon_from_shopify_frontend():
    """Extract favicon from Shopify store's public frontend"""
    
    shop_url = "https://protonord.myshopify.com"
    
    try:
        print(f"🌐 Fetching homepage from {shop_url}...")
        
        # Get the homepage
        response = requests.get(shop_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        html_content = response.text
        
        # Look for favicon links in HTML
        favicon_patterns = [
            r'<link[^>]*rel=["\'](?:icon|shortcut icon|apple-touch-icon)["\'][^>]*href=["\']([^"\']+)["\']',
            r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\'](?:icon|shortcut icon|apple-touch-icon)["\']',
            r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
        ]
        
        favicon_urls = []
        
        for pattern in favicon_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                # Convert relative URLs to absolute
                if match.startswith('//'):
                    match = 'https:' + match
                elif match.startswith('/'):
                    match = urljoin(shop_url, match)
                elif not match.startswith('http'):
                    match = urljoin(shop_url, match)
                
                favicon_urls.append(match)
        
        if favicon_urls:
            print(f"🎯 Found {len(favicon_urls)} potential favicon/logo URLs:")
            for url in favicon_urls:
                print(f"  - {url}")
            
            # Try to download the first valid favicon
            for url in favicon_urls:
                try:
                    print(f"⬇️ Downloading favicon from: {url}")
                    
                    favicon_response = requests.get(url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    })
                    favicon_response.raise_for_status()
                    
                    # Check if it's actually an image
                    content_type = favicon_response.headers.get('content-type', '')
                    if 'image' in content_type:
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
                            f.write(favicon_response.content)
                        
                        print(f"✅ Successfully downloaded favicon to {favicon_path}")
                        print(f"📏 File size: {len(favicon_response.content)} bytes")
                        print(f"🎨 Content type: {content_type}")
                        return True
                    
                except Exception as e:
                    print(f"⚠️ Failed to download {url}: {e}")
                    continue
        
        # If no favicon found in HTML, try common default locations
        default_favicon_urls = [
            f"{shop_url}/favicon.ico",
            f"{shop_url}/favicon.png",
            f"{shop_url}/apple-touch-icon.png",
            f"{shop_url}/assets/favicon.ico",
            f"{shop_url}/cdn/shop/files/favicon.ico",
        ]
        
        print("🔍 Trying common favicon locations...")
        for url in default_favicon_urls:
            try:
                print(f"⬇️ Trying: {url}")
                favicon_response = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                if favicon_response.status_code == 200:
                    content_type = favicon_response.headers.get('content-type', '')
                    if 'image' in content_type:
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
                            f.write(favicon_response.content)
                        
                        print(f"✅ Successfully downloaded favicon from {url}")
                        print(f"📏 File size: {len(favicon_response.content)} bytes")
                        print(f"🎨 Content type: {content_type}")
                        return True
                
            except Exception as e:
                print(f"⚠️ Failed to download {url}: {e}")
                continue
        
        print("❌ No favicon found in Shopify store frontend")
        return False
        
    except Exception as e:
        print(f"❌ Error fetching favicon from Shopify frontend: {e}")
        return False

if __name__ == "__main__":
    print("🛍️ Extracting favicon from Shopify store frontend...")
    
    if extract_favicon_from_shopify_frontend():
        print("🎉 Favicon successfully updated from Shopify!")
    else:
        print("❌ Failed to extract favicon from Shopify frontend")
        print("💡 You may need to manually download the favicon from the store")