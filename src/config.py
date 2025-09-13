import os
from dotenv import load_dotenv

load_dotenv()

# Shopify configuration
SHOPIFY_SHOP = os.getenv("SHOPIFY_SHOP", "")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")

# Cloud storage configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "127.0.0.1:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "products")
MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"

# GitHub configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "")

# Local configuration
DATA_ROOT = os.getenv("DATA_ROOT", "catalog")

def validate():
    """Validate required environment variables"""
    missing = []
    if not SHOPIFY_SHOP: 
        missing.append("SHOPIFY_SHOP")
    if not SHOPIFY_ACCESS_TOKEN: 
        missing.append("SHOPIFY_ACCESS_TOKEN")
    if not MINIO_ACCESS_KEY: 
        missing.append("MINIO_ACCESS_KEY")
    if not MINIO_SECRET_KEY: 
        missing.append("MINIO_SECRET_KEY")
    
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")