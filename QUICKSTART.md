# Quick Start Guide

## 🚀 Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Required settings in `.env`:
- `SHOPIFY_SHOP` - Your Shopify store URL (yourstore.myshopify.com)
- `SHOPIFY_ACCESS_TOKEN` - Admin API access token from a Custom App
- `MINIO_ENDPOINT` - MinIO server address (e.g., localhost:9000)
- `MINIO_ACCESS_KEY` - MinIO access key
- `MINIO_SECRET_KEY` - MinIO secret key
- `MINIO_BUCKET` - Bucket name for storing files (e.g., "products")

### 3. Setup MinIO Server

Install and run MinIO locally:

```bash
# Download MinIO (Linux)
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio

# Start MinIO server
./minio server ./minio-data --console-address ":9001"
```

Access MinIO console at http://localhost:9001 (default: minioadmin/minioadmin)

### 4. Setup Shopify Custom App

1. Go to your Shopify Admin → Apps → App and sales channel settings
2. Click "Develop apps" → "Create an app"
3. Configure Admin API access scopes:
   - `read_products`
   - `write_products` 
   - `read_files`
   - `write_files`
4. Install the app and copy the Admin API access token

## 🔄 Usage

### Bootstrap Catalog from Shopify

Import all existing products from Shopify:

```bash
python main.py bootstrap
```

This creates:
- Local folder structure in `catalog/`
- Product JSON files with metadata
- Images stored in MinIO
- Git-ready structure

### Sync Changes to Shopify

Sync all local changes back to Shopify:

```bash
python main.py sync
```

Sync a specific product:

```bash
python main.py sync product-handle
```

### Create New Product

```bash
python main.py new "My New Product" --type "Electronics" --vendor "ACME Corp"
```

### Check Status

```bash
python main.py status
```

## 📁 Folder Structure

After bootstrap, you'll have:

```
catalog/
├── product-handle-1/
│   ├── product.json      # Shopify product data
│   ├── description.md    # Editable description
│   ├── README.md        # Product documentation
│   ├── images/          # Product images (in MinIO)
│   ├── cad/            # CAD files (in MinIO)
│   └── documentation/   # Additional docs
├── product-handle-2/
│   └── ...
└── catalog_summary.json  # Overview
```

## 🔧 Workflow

1. **Bootstrap**: Import existing products from Shopify
2. **Edit**: Modify `product.json` or `description.md` files
3. **Upload**: Add files to MinIO via web interface or CLI
4. **Sync**: Push changes back to Shopify
5. **Commit**: Save changes to Git for version control

## 🆘 Troubleshooting

- **Connection errors**: Check `.env` file and network connectivity
- **Permission errors**: Verify Shopify app scopes and MinIO credentials
- **Missing products**: Ensure products exist in Shopify and are not archived
- **File upload issues**: Check MinIO bucket permissions and storage space

## 🔗 Next Steps

- Set up Git repository and push catalog
- Configure GitHub Actions for automated syncing
- Add webhook for real-time updates
- Integrate with CAD software plugins