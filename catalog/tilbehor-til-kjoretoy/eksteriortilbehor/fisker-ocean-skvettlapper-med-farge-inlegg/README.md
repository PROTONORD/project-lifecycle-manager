# Fisker Ocean Front Skvettlapper v2

**Handle:** `fisker-ocean-skvettlapper-med-farge-inlegg`  
**Status:** active  
**Leverandør:** PROTONORD

## 📁 Filstruktur (Lagret i MinIO)

Alle produktfiler er lagret i MinIO object storage og kan nås via:

### 🔗 Direktelenker:
- **Produktdata:** [product.json](http://127.0.0.1:9000/products/fisker-ocean-skvettlapper-med-farge-inlegg/product.json)
- **Beskrivelse:** [description.md](http://127.0.0.1:9000/products/fisker-ocean-skvettlapper-med-farge-inlegg/description.md)
- **Bilder:** [images/](http://127.0.0.1:9000/products/fisker-ocean-skvettlapper-med-farge-inlegg/images/)
- **CAD-filer:** [cad-files/](http://127.0.0.1:9000/products/fisker-ocean-skvettlapper-med-farge-inlegg/cad-files/)
- **Dokumentasjon:** [documentation/](http://127.0.0.1:9000/products/fisker-ocean-skvettlapper-med-farge-inlegg/documentation/)

### 📊 MinIO Web Interface:
Tilgang til filer via MinIO web interface på:
`http://127.0.0.1:9000:9001`

**Mappe:** `products/fisker-ocean-skvettlapper-med-farge-inlegg/`

### 🔄 Synkronisering:
- **GitHub → MinIO:** Referanser og metadata
- **MinIO → Shopify:** Produktdata og bilder synkroniseres automatisk
- **Last oppdatert:** 2025-09-11 19:45:25

## 💡 Redigering:
1. **Bilder/CAD-filer:** Last opp direkte til MinIO via web interface
2. **Produktdata:** Rediger JSON-filer i MinIO og kjør synkronisering
3. **Synkroniser til Shopify:** `python tools/sync_product_data.py --to-shopify --product fisker-ocean-skvettlapper-med-farge-inlegg`
