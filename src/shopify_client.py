import requests
from typing import Dict, List, Optional

class ShopifyClient:
    """Client for interacting with Shopify Admin API"""
    
    def __init__(self, shop: str, token: str):
        self.base_url = f"https://{shop}/admin/api/2024-07"
        self.session = requests.Session()
        self.session.headers.update({
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def list_products(self, limit: int = 250) -> List[Dict]:
        """Fetch all products from Shopify with pagination"""
        url = f"{self.base_url}/products.json"
        params = {"limit": limit}
        products = []
        
        while True:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json().get("products", [])
            products.extend(data)
            
            # Handle pagination using Link header
            link_header = response.headers.get("Link", "")
            next_url = self._parse_next_link(link_header)
            
            if not next_url:
                break
                
            url = next_url
            params = {}
            
        return products

    def get_product(self, product_id: int) -> Dict:
        """Get a single product by ID"""
        url = f"{self.base_url}/products/{product_id}.json"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("product", {})

    def update_product(self, product_id: int, product_data: Dict) -> Dict:
        """Update a product"""
        url = f"{self.base_url}/products/{product_id}.json"
        payload = {"product": product_data}
        response = self.session.put(url, json=payload)
        response.raise_for_status()
        return response.json().get("product", {})

    def create_product(self, product_data: Dict) -> Dict:
        """Create a new product"""
        url = f"{self.base_url}/products.json"
        payload = {"product": product_data}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("product", {})

    def get_collections(self, limit: int = 250) -> List[Dict]:
        """Fetch all collections from Shopify (both smart and custom collections)"""
        collections = []
        
        # Get smart collections
        url = f"{self.base_url}/smart_collections.json"
        params = {"limit": limit}
        
        while True:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json().get("smart_collections", [])
            collections.extend(data)
            
            # Handle pagination using Link header
            link_header = response.headers.get("Link", "")
            if not link_header:
                break
                
            next_url = self._parse_next_link(link_header)
            if not next_url:
                break
                
            url = next_url
            params = {}
        
        # Get custom collections
        url = f"{self.base_url}/custom_collections.json"
        params = {"limit": limit}
        
        while True:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json().get("custom_collections", [])
            collections.extend(data)
            
            # Handle pagination using Link header
            link_header = response.headers.get("Link", "")
            if not link_header:
                break
                
            next_url = self._parse_next_link(link_header)
            if not next_url:
                break
                
            url = next_url
            params = {}
            
        return collections

    def get_collection_products(self, collection_id: int, limit: int = 250) -> List[Dict]:
        """Fetch products in a specific collection"""
        url = f"{self.base_url}/collections/{collection_id}/products.json"
        params = {"limit": limit}
        products = []
        
        while True:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json().get("products", [])
            products.extend(data)
            
            # Handle pagination using Link header
            link_header = response.headers.get("Link", "")
            if not link_header:
                break
                
            next_url = self._parse_next_link(link_header)
            if not next_url:
                break
                
            url = next_url
            params = {}
            
        return products

    def get_shop_info(self) -> Dict:
        """Get shop information including logo and other assets"""
        url = f"{self.base_url}/shop.json"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("shop", {})

    def get_themes(self) -> List[Dict]:
        """Get all themes for the shop"""
        url = f"{self.base_url}/themes.json"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("themes", [])

    def get_theme_assets(self, theme_id: int, asset_key: str = None) -> Dict:
        """Get theme assets (can be used to find favicon or logo files)"""
        url = f"{self.base_url}/themes/{theme_id}/assets.json"
        params = {}
        if asset_key:
            params["asset[key]"] = asset_key
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _parse_next_link(self, link_header: str) -> Optional[str]:
        """Parse the next URL from Link header (RFC5988)"""
        for part in link_header.split(","):
            part = part.strip()
            if 'rel="next"' in part:
                start = part.find("<") + 1
                end = part.find(">")
                return part[start:end]
        return None