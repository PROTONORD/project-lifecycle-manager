# Philips Hue lysbryter foring

**Handle:** `philips-hue-lysbryter-foring`  
**Status:** active  
**Leverandør:** PROTONORD

## 📁 Filstruktur (Lagret i MinIO)

Alle produktfiler er lagret i MinIO object storage og kan nås via:

### 🔗 Direktelenker:
- **Produktdata:** [product.json](http://127.0.0.1:9000/products/philips-hue-lysbryter-foring/product.json)
- **Beskrivelse:** [description.md](http://127.0.0.1:9000/products/philips-hue-lysbryter-foring/description.md)
- **Bilder:** [images/](http://127.0.0.1:9000/products/philips-hue-lysbryter-foring/images/)
- **CAD-filer:** [cad-files/](http://127.0.0.1:9000/products/philips-hue-lysbryter-foring/cad-files/)
- **Dokumentasjon:** [documentation/](http://127.0.0.1:9000/products/philips-hue-lysbryter-foring/documentation/)

### 📊 MinIO Web Interface:
Tilgang til filer via MinIO web interface på:
`http://127.0.0.1:9000:9001`

**Mappe:** `products/philips-hue-lysbryter-foring/`

### 🔄 Synkronisering:
- **GitHub → MinIO:** Referanser og metadata
- **MinIO → Shopify:** Produktdata og bilder synkroniseres automatisk
- **Last oppdatert:** 2025-09-11 19:45:26

## 💡 Redigering:
1. **Bilder/CAD-filer:** Last opp direkte til MinIO via web interface
2. **Produktdata:** Rediger JSON-filer i MinIO og kjør synkronisering
3. **Synkroniser til Shopify:** `python tools/sync_product_data.py --to-shopify --product philips-hue-lysbryter-foring`
