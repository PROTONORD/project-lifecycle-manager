# Audi Q4 E-tron LÅS vær og snødeksel V2 (passer både V1 og V2)

**Handle:** `audi-q4-las-vaer-og-snodeksel-v2-passer-bade-v1-og-v2`  
**Status:** archived  
**Leverandør:** PROTONORD

## 📁 Filstruktur (Lagret i MinIO)

Alle produktfiler er lagret i MinIO object storage og kan nås via:

### 🔗 Direktelenker:
- **Produktdata:** [product.json](http://127.0.0.1:9000/products/audi-q4-las-vaer-og-snodeksel-v2-passer-bade-v1-og-v2/product.json)
- **Beskrivelse:** [description.md](http://127.0.0.1:9000/products/audi-q4-las-vaer-og-snodeksel-v2-passer-bade-v1-og-v2/description.md)
- **Bilder:** [images/](http://127.0.0.1:9000/products/audi-q4-las-vaer-og-snodeksel-v2-passer-bade-v1-og-v2/images/)
- **CAD-filer:** [cad-files/](http://127.0.0.1:9000/products/audi-q4-las-vaer-og-snodeksel-v2-passer-bade-v1-og-v2/cad-files/)
- **Dokumentasjon:** [documentation/](http://127.0.0.1:9000/products/audi-q4-las-vaer-og-snodeksel-v2-passer-bade-v1-og-v2/documentation/)

### 📊 MinIO Web Interface:
Tilgang til filer via MinIO web interface på:
`http://127.0.0.1:9000:9001`

**Mappe:** `products/audi-q4-las-vaer-og-snodeksel-v2-passer-bade-v1-og-v2/`

### 🔄 Synkronisering:
- **GitHub → MinIO:** Referanser og metadata
- **MinIO → Shopify:** Produktdata og bilder synkroniseres automatisk
- **Last oppdatert:** 2025-09-11 19:45:25

## 💡 Redigering:
1. **Bilder/CAD-filer:** Last opp direkte til MinIO via web interface
2. **Produktdata:** Rediger JSON-filer i MinIO og kjør synkronisering
3. **Synkroniser til Shopify:** `python tools/sync_product_data.py --to-shopify --product audi-q4-las-vaer-og-snodeksel-v2-passer-bade-v1-og-v2`
