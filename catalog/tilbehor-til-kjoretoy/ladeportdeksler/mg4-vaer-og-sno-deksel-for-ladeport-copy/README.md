# MG Marvel R

**Handle:** `mg4-vaer-og-sno-deksel-for-ladeport-copy`  
**Status:** active  
**Leverandør:** PROTONORD

## 📁 Filstruktur (Lagret i cloud backup)

Alle produktfiler er lagret i cloud backup repository og kan nås via:

### 🔗 Direktelenker:
- **Produktdata:** [product.json](http://127.0.0.1:9000/products/mg4-vaer-og-sno-deksel-for-ladeport-copy/product.json)
- **Beskrivelse:** [description.md](http://127.0.0.1:9000/products/mg4-vaer-og-sno-deksel-for-ladeport-copy/description.md)
- **Bilder:** [images/](http://127.0.0.1:9000/products/mg4-vaer-og-sno-deksel-for-ladeport-copy/images/)
- **CAD-filer:** [cad-files/](http://127.0.0.1:9000/products/mg4-vaer-og-sno-deksel-for-ladeport-copy/cad-files/)
- **Dokumentasjon:** [documentation/](http://127.0.0.1:9000/products/mg4-vaer-og-sno-deksel-for-ladeport-copy/documentation/)

### 📊 cloud backup Web Interface:
Tilgang til filer via cloud backup web interface på:
`http://127.0.0.1:9000:9001`

**Mappe:** `products/mg4-vaer-og-sno-deksel-for-ladeport-copy/`

### 🔄 Synkronisering:
- **GitHub → cloud backup:** Referanser og metadata
- **cloud backup → Shopify:** Produktdata og bilder synkroniseres automatisk
- **Last oppdatert:** 2025-09-11 19:45:25

## 💡 Redigering:
1. **Bilder/CAD-filer:** Last opp direkte til cloud backup via web interface
2. **Produktdata:** Rediger JSON-filer i cloud backup og kjør synkronisering
3. **Synkroniser til Shopify:** `python tools/sync_product_data.py --to-shopify --product mg4-vaer-og-sno-deksel-for-ladeport-copy`
