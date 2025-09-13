# Lexus UX300e vær og snø deksel for ladeport

**Handle:** `lexus-ux300e-vaer-og-sno-deksel-for-ladeport-1`  
**Status:** active  
**Leverandør:** PROTONORD

## 📁 Filstruktur (Lagret i MinIO)

Alle produktfiler er lagret i MinIO object storage og kan nås via:

### 🔗 Direktelenker:
- **Produktdata:** [product.json](http://127.0.0.1:9000/products/lexus-ux300e-vaer-og-sno-deksel-for-ladeport-1/product.json)
- **Beskrivelse:** [description.md](http://127.0.0.1:9000/products/lexus-ux300e-vaer-og-sno-deksel-for-ladeport-1/description.md)
- **Bilder:** [images/](http://127.0.0.1:9000/products/lexus-ux300e-vaer-og-sno-deksel-for-ladeport-1/images/)
- **CAD-filer:** [cad-files/](http://127.0.0.1:9000/products/lexus-ux300e-vaer-og-sno-deksel-for-ladeport-1/cad-files/)
- **Dokumentasjon:** [documentation/](http://127.0.0.1:9000/products/lexus-ux300e-vaer-og-sno-deksel-for-ladeport-1/documentation/)

### 📊 MinIO Web Interface:
Tilgang til filer via MinIO web interface på:
`http://127.0.0.1:9000:9001`

**Mappe:** `products/lexus-ux300e-vaer-og-sno-deksel-for-ladeport-1/`

### 🔄 Synkronisering:
- **GitHub → MinIO:** Referanser og metadata
- **MinIO → Shopify:** Produktdata og bilder synkroniseres automatisk
- **Last oppdatert:** 2025-09-11 19:45:25

## 💡 Redigering:
1. **Bilder/CAD-filer:** Last opp direkte til MinIO via web interface
2. **Produktdata:** Rediger JSON-filer i MinIO og kjør synkronisering
3. **Synkroniser til Shopify:** `python tools/sync_product_data.py --to-shopify --product lexus-ux300e-vaer-og-sno-deksel-for-ladeport-1`
