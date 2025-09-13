# Gåstol reservedel til håndtak justering

**Handle:** `gastol-reservedel-til-handtak-justering`  
**Status:** active  
**Leverandør:** PROTONORD

## 📁 Filstruktur (Lagret i MinIO)

Alle produktfiler er lagret i MinIO object storage og kan nås via:

### 🔗 Direktelenker:
- **Produktdata:** [product.json](http://127.0.0.1:9000/products/gastol-reservedel-til-handtak-justering/product.json)
- **Beskrivelse:** [description.md](http://127.0.0.1:9000/products/gastol-reservedel-til-handtak-justering/description.md)
- **Bilder:** [images/](http://127.0.0.1:9000/products/gastol-reservedel-til-handtak-justering/images/)
- **CAD-filer:** [cad-files/](http://127.0.0.1:9000/products/gastol-reservedel-til-handtak-justering/cad-files/)
- **Dokumentasjon:** [documentation/](http://127.0.0.1:9000/products/gastol-reservedel-til-handtak-justering/documentation/)

### 📊 MinIO Web Interface:
Tilgang til filer via MinIO web interface på:
`http://127.0.0.1:9000:9001`

**Mappe:** `products/gastol-reservedel-til-handtak-justering/`

### 🔄 Synkronisering:
- **GitHub → MinIO:** Referanser og metadata
- **MinIO → Shopify:** Produktdata og bilder synkroniseres automatisk
- **Last oppdatert:** 2025-09-11 19:45:25

## 💡 Redigering:
1. **Bilder/CAD-filer:** Last opp direkte til MinIO via web interface
2. **Produktdata:** Rediger JSON-filer i MinIO og kjør synkronisering
3. **Synkroniser til Shopify:** `python tools/sync_product_data.py --to-shopify --product gastol-reservedel-til-handtak-justering`
