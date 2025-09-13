#!/usr/bin/env python3
"""
ProtoNord Shopify Data Synkronisering
Henter komplett data fra protonord.shopify.com og lagrer til JSON.
"""

import json
import requests
import datetime
import logging
import configparser
import time
import os
import sys
from pathlib import Path
from urllib.parse import urljoin
from dotenv import load_dotenv

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"shopify_sync_{datetime.date.today()}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class ShopifyAPI:
    def __init__(self, config_file):
        """Initialiser Shopify API klient"""
        # Last environment variables
        load_dotenv(Path(__file__).parent.parent / '.env')
        
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # Hent API legitimasjon fra environment variables
        self.shop_url = os.getenv('SHOPIFY_SHOP_URL', self.config.get('shopify', 'shop_url', fallback=''))
        self.api_version = os.getenv('SHOPIFY_API_VERSION', self.config.get('shopify', 'api_version', fallback='2023-10'))
        self.access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')
        
        if not self.access_token:
            raise ValueError("❌ SHOPIFY_ACCESS_TOKEN må være satt i .env fil eller environment variables")
        
        if not self.shop_url:
            raise ValueError("❌ SHOPIFY_SHOP_URL må være satt i .env fil eller konfigurasjon")
        
        # API base URL
        self.base_url = f"https://{self.shop_url}/admin/api/{self.api_version}/"
        
        # Rate limiting
        self.requests_per_second = self.config.getint('sync', 'requests_per_second', fallback=2)
        self.max_retries = self.config.getint('sync', 'max_retries', fallback=3)
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'X-Shopify-Access-Token': self.access_token,
            'Content-Type': 'application/json'
        })
        
        logger.info(f"🔌 Shopify API klient initialisert for {self.shop_url}")

    def _make_request(self, endpoint, params=None):
        """Gjør API-forespørsel med rate limiting og retry logikk"""
        url = urljoin(self.base_url, endpoint)
        
        for attempt in range(self.max_retries):
            try:
                # Rate limiting
                time.sleep(1 / self.requests_per_second)
                
                response = self.session.get(url, params=params, timeout=30)
                
                # Sjekk Shopify rate limit headers
                if 'X-Shopify-Shop-Api-Call-Limit' in response.headers:
                    call_limit = response.headers['X-Shopify-Shop-Api-Call-Limit']
                    logger.debug(f"API Call Limit: {call_limit}")
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limited
                    wait_time = int(response.headers.get('Retry-After', 5))
                    logger.warning(f"⏳ Rate limited, venter {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"❌ API feil {response.status_code}: {response.text}")
                    response.raise_for_status()
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"⚠️ Forsøk {attempt + 1}/{self.max_retries} feilet: {e}")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return None

    def get_products(self, limit=250):
        """Hent alle produkter (ekskluderer arkiverte)"""
        logger.info("📦 Henter produkter...")
        products = []
        params = {
            'limit': limit,
            'status': 'active'  # Hent kun aktive produkter, ikke arkiverte
        }
        
        while True:
            data = self._make_request('products.json', params)
            if not data or 'products' not in data:
                break
                
            batch_products = data['products']
            products.extend(batch_products)
            logger.info(f"   Hentet {len(batch_products)} produkter (totalt: {len(products)})")
            
            # Pagination
            if len(batch_products) < limit:
                break
            
            # Use the last product ID for pagination
            if batch_products:
                params['since_id'] = batch_products[-1]['id']
        
        logger.info(f"✅ Hentet totalt {len(products)} aktive produkter (arkiverte utelukket)")
        return products

    def get_orders(self, days_back=30, limit=250):
        """Hent bestillinger fra de siste N dagene"""
        logger.info(f"🛒 Henter bestillinger (siste {days_back} dager)...")
        
        # Beregn dato
        since_date = datetime.datetime.now() - datetime.timedelta(days=days_back)
        since_str = since_date.strftime('%Y-%m-%dT%H:%M:%S')
        
        orders = []
        params = {
            'limit': limit,
            'status': 'any',
            'created_at_min': since_str
        }
        
        while True:
            data = self._make_request('orders.json', params)
            if not data or 'orders' not in data:
                break
                
            batch_orders = data['orders']
            orders.extend(batch_orders)
            logger.info(f"   Hentet {len(batch_orders)} bestillinger (totalt: {len(orders)})")
            
            # Pagination
            if len(batch_orders) < limit:
                break
                
            # Use the last order ID for pagination
            if batch_orders:
                params['since_id'] = batch_orders[-1]['id']
        
        logger.info(f"✅ Hentet totalt {len(orders)} bestillinger")
        return orders

    def get_customers(self, days_back=90, limit=250):
        """Hent kunder"""
        logger.info(f"👥 Henter kunder (siste {days_back} dager)...")
        
        # Beregn dato
        since_date = datetime.datetime.now() - datetime.timedelta(days=days_back)
        since_str = since_date.strftime('%Y-%m-%dT%H:%M:%S')
        
        customers = []
        params = {
            'limit': limit,
            'created_at_min': since_str
        }
        
        while True:
            data = self._make_request('customers.json', params)
            if not data or 'customers' not in data:
                break
                
            batch_customers = data['customers']
            customers.extend(batch_customers)
            logger.info(f"   Hentet {len(batch_customers)} kunder (totalt: {len(customers)})")
            
            # Pagination
            if len(batch_customers) < limit:
                break
                
            if batch_customers:
                params['since_id'] = batch_customers[-1]['id']
        
        logger.info(f"✅ Hentet totalt {len(customers)} kunder")
        return customers

    def get_collections(self):
        """Hent produktkolleksjoner"""
        logger.info("📁 Henter kolleksjoner...")
        
        # Smart collections
        smart_data = self._make_request('smart_collections.json')
        smart_collections = smart_data.get('smart_collections', []) if smart_data else []
        
        # Custom collections  
        custom_data = self._make_request('custom_collections.json')
        custom_collections = custom_data.get('custom_collections', []) if custom_data else []
        
        collections = {
            'smart_collections': smart_collections,
            'custom_collections': custom_collections
        }
        
        total = len(smart_collections) + len(custom_collections)
        logger.info(f"✅ Hentet {total} kolleksjoner ({len(smart_collections)} smarte, {len(custom_collections)} tilpassede)")
        return collections

    def get_inventory_levels(self):
        """Hent inventory locations og levels"""
        logger.info("📋 Henter inventory data...")
        
        # Locations
        locations_data = self._make_request('locations.json')
        locations = locations_data.get('locations', []) if locations_data else []
        
        inventory_data = {
            'locations': locations,
            'levels': []
        }
        
        # Inventory levels for each location
        for location in locations:
            location_id = location['id']
            levels_data = self._make_request(f'inventory_levels.json?location_ids={location_id}')
            if levels_data and 'inventory_levels' in levels_data:
                inventory_data['levels'].extend(levels_data['inventory_levels'])
        
        logger.info(f"✅ Hentet inventory for {len(locations)} lokasjoner")
        return inventory_data

    def get_shop_info(self):
        """Hent butikkinformasjon"""
        logger.info("🏪 Henter butikkinformasjon...")
        
        shop_data = self._make_request('shop.json')
        shop_info = shop_data.get('shop', {}) if shop_data else {}
        
        logger.info(f"✅ Hentet butikkinformasjon for {shop_info.get('name', 'ukjent')}")
        return shop_info

def sync_shopify_data():
    """Hovedfunksjon for å synkronisere Shopify data"""
    logger.info("🚀 Starter ProtoNord Shopify synkronisering...")
    
    # Les konfigurasjon
    script_dir = Path(__file__).parent.parent
    config_file = script_dir / "config/shopify_config.ini"
    
    if not config_file.exists():
        logger.error(f"❌ Konfigurasjonsfil ikke funnet: {config_file}")
        return False
    
    try:
        # Initialiser API
        api = ShopifyAPI(config_file)
        
        # Les sync-konfigurasjon
        config = configparser.ConfigParser()
        config.read(config_file)
        
        # Samle all data
        shopify_data = {
            'metadata': {
                'shop': api.shop_url,
                'sync_time': datetime.datetime.now().isoformat(),
                'api_version': api.api_version
            }
        }
        
        # Hent butikkinformasjon først
        shopify_data['shop_info'] = api.get_shop_info()
        
        # Hent data basert på konfigurasjon
        if config.getboolean('sync', 'products', fallback=True):
            shopify_data['products'] = api.get_products()
        
        if config.getboolean('sync', 'orders', fallback=True):
            days_back = config.getint('sync', 'orders_days_back', fallback=30)
            shopify_data['orders'] = api.get_orders(days_back)
        
        if config.getboolean('sync', 'customers', fallback=True):
            days_back = config.getint('sync', 'customers_days_back', fallback=90)
            shopify_data['customers'] = api.get_customers(days_back)
        
        if config.getboolean('sync', 'collections', fallback=True):
            shopify_data['collections'] = api.get_collections()
        
        if config.getboolean('sync', 'inventory', fallback=True):
            shopify_data['inventory'] = api.get_inventory_levels()
        
        # Generer statistikk
        stats = {
            'products': len(shopify_data.get('products', [])),
            'orders': len(shopify_data.get('orders', [])),
            'customers': len(shopify_data.get('customers', [])),
            'smart_collections': len(shopify_data.get('collections', {}).get('smart_collections', [])),
            'custom_collections': len(shopify_data.get('collections', {}).get('custom_collections', [])),
            'locations': len(shopify_data.get('inventory', {}).get('locations', [])),
            'inventory_levels': len(shopify_data.get('inventory', {}).get('levels', []))
        }
        
        shopify_data['statistics'] = stats
        
        # Opprett public versjon (uten sensitive opplysninger)
        public_data = {
            'shop_info': shopify_data.get('shop_info'),
            'products': shopify_data.get('products'),
            'collections': shopify_data.get('collections'),
            'inventory': shopify_data.get('inventory'),
            'statistics': stats,
            'last_updated': datetime.datetime.now().isoformat()
        }
        
        # Legg til sanitized orders (uten navn og adresser)
        if 'orders' in shopify_data:
            public_orders = []
            for order in shopify_data['orders']:
                public_order = {
                    'id': order.get('id'),
                    'created_at': order.get('created_at'),
                    'total_price': order.get('total_price'),
                    'currency': order.get('currency'),
                    'financial_status': order.get('financial_status'),
                    'fulfillment_status': order.get('fulfillment_status'),
                    'order_number': order.get('order_number'),
                    'line_items_count': len(order.get('line_items', [])),
                    'tags': order.get('tags', ''),
                    'source_name': order.get('source_name'),
                    'line_items': [{ # Behold produktinfo, men fjern personlige detaljer
                        'id': item.get('id'),
                        'title': item.get('title'),
                        'quantity': item.get('quantity'),
                        'price': item.get('price'),
                        'sku': item.get('sku'),
                        'product_id': item.get('product_id'),
                        'variant_id': item.get('variant_id')
                    } for item in order.get('line_items', [])]
                }
                public_orders.append(public_order)
            public_data['orders'] = public_orders
        
        # Legg til sanitized customers (uten navn og kontaktinfo)
        if 'customers' in shopify_data:
            public_customers = []
            for customer in shopify_data['customers']:
                public_customer = {
                    'id': customer.get('id'),
                    'created_at': customer.get('created_at'),
                    'updated_at': customer.get('updated_at'),
                    'orders_count': customer.get('orders_count', 0),
                    'total_spent': customer.get('total_spent'),
                    'state': customer.get('state'),
                    'verified_email': customer.get('verified_email'),
                    'tags': customer.get('tags', ''),
                    'currency': customer.get('currency')
                }
                public_customers.append(public_customer)
            public_data['customers'] = public_customers
        
        # Sensitive data (full details for cloud-only storage)
        sensitive_data = {
            'shop_info': shopify_data.get('shop_info'),
            'orders_detailed': shopify_data.get('orders', []),
            'customers_detailed': shopify_data.get('customers', []),
            'statistics': stats,
            'last_updated': datetime.datetime.now().isoformat()
        }
        
        # Lagre til JSON filer
        output_dir = script_dir / "data/shopify"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Timestamped filer
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        public_timestamped_file = output_dir / f"protonord_shopify_public_{timestamp}.json"
        sensitive_timestamped_file = output_dir / f"protonord_shopify_sensitive_{timestamp}.json"
        
        # Latest filer
        public_latest_file = output_dir / "protonord_shopify_latest.json"
        sensitive_latest_file = output_dir / "protonord_shopify_sensitive_latest.json"
        
        # JSON innstillinger
        json_settings = {
            'indent': 2 if config.getboolean('output', 'pretty_print', fallback=True) else None,
            'ensure_ascii': False
        }
        
        # Lagre public filer (for web visning)
        for file_path in [public_timestamped_file, public_latest_file]:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(public_data, f, **json_settings)
        
        # Lagre sensitive filer (kun for cloud storage)
        for file_path in [sensitive_timestamped_file, sensitive_latest_file]:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(sensitive_data, f, **json_settings)
        
        logger.info("📊 SHOPIFY SYNC STATISTIKK:")
        for key, value in stats.items():
            logger.info(f"   {key}: {value}")
        
        logger.info(f"💾 Data lagret til:")
        logger.info(f"   Public Timestamped: {public_timestamped_file}")
        logger.info(f"   Public Latest: {public_latest_file}")
        logger.info(f"   Sensitive Timestamped: {sensitive_timestamped_file}")
        logger.info(f"   Sensitive Latest: {sensitive_latest_file}")
        
        # Upload til cloud storage
        logger.info("☁️ Starter cloud upload...")
        try:
            from shopify_cloud_upload import upload_to_cloud, cleanup_old_files
            
            # Upload både public og sensitive filer til cloud
            public_upload_success = upload_to_cloud(public_latest_file)
            sensitive_upload_success = upload_to_cloud(sensitive_latest_file)
            
            if public_upload_success and sensitive_upload_success:
                logger.info("✅ Cloud upload fullført!")
                
                # Cleanup gamle lokale filer
                cleanup_old_files(days_to_keep=7)
            else:
                logger.warning("⚠️ Cloud upload delvis feilet, men data er lagret lokalt")
                
        except ImportError:
            logger.warning("⚠️ Cloud upload modul ikke tilgjengelig")
        except Exception as e:
            logger.error(f"❌ Cloud upload feilet: {e}")
        
        # Kopier public fil til static mappe for web visning
        try:
            static_dir = script_dir / "static/data/shopify"
            static_dir.mkdir(parents=True, exist_ok=True)
            static_public_file = static_dir / "protonord_shopify_public.json"
            
            import shutil
            shutil.copy2(public_latest_file, static_public_file)
            logger.info(f"📂 Public fil kopiert til static: {static_public_file}")
            
        except Exception as e:
            logger.error(f"❌ Feil ved kopiering til static mappe: {e}")
        
        logger.info("🎉 Shopify synkronisering fullført!")
        return True, public_latest_file
        
    except Exception as e:
        logger.error(f"💥 Shopify sync feilet: {e}")
        return False, None

if __name__ == "__main__":
    success, output_file = sync_shopify_data()
    sys.exit(0 if success else 1)