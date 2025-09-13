# BMW X5 (G05) Plug-in Hybrid vær og snø deksel for ladeport

**Handle:** `bmw-x5-hybrid-vaer-og-sno-deksel-for-ladeport`  
**Status:** active  
**Leverandør:** PROTONORD

## 📁 Filstruktur (Lagret i MinIO)

Alle produktfiler er lagret i MinIO object storage og kan nås via:

### 🔗 Direktelenker:
- **Produktdata:** [product.json](http://127.0.0.1:9000/products/bmw-x5-hybrid-vaer-og-sno-deksel-for-ladeport/product.json)
- **Beskrivelse:** [description.md](http://127.0.0.1:9000/products/bmw-x5-hybrid-vaer-og-sno-deksel-for-ladeport/description.md)
- **Bilder:** [images/](http://127.0.0.1:9000/products/bmw-x5-hybrid-vaer-og-sno-deksel-for-ladeport/images/)
- **CAD-filer:** [cad-files/](http://127.0.0.1:9000/products/bmw-x5-hybrid-vaer-og-sno-deksel-for-ladeport/cad-files/)
- **Dokumentasjon:** [documentation/](http://127.0.0.1:9000/products/bmw-x5-hybrid-vaer-og-sno-deksel-for-ladeport/documentation/)

### 📊 MinIO Web Interface:
Tilgang til filer via MinIO web interface på:
`http://127.0.0.1:9000:9001`

**Mappe:** `products/bmw-x5-hybrid-vaer-og-sno-deksel-for-ladeport/`

### 🔄 Synkronisering:
- **GitHub → MinIO:** Referanser og metadata
- **MinIO → Shopify:** Produktdata og bilder synkroniseres automatisk
- **Last oppdatert:** 2025-09-11 19:45:25

## 💡 Redigering:
1. **Bilder/CAD-filer:** Last opp direkte til MinIO via web interface
2. **Produktdata:** Rediger JSON-filer i MinIO og kjør synkronisering
3. **Synkroniser til Shopify:** `python tools/sync_product_data.py --to-shopify --product bmw-x5-hybrid-vaer-og-sno-deksel-for-ladeport`
