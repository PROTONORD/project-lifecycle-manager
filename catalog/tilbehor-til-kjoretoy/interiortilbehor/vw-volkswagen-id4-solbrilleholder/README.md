# VolksWagen ID.4 Solbrilleholder

**Handle:** `vw-volkswagen-id4-solbrilleholder`  
**Status:** active  
**Leverandør:** Yurik Accessories

## 📁 Filstruktur (Lagret i MinIO)

Alle produktfiler er lagret i MinIO object storage og kan nås via:

### 🔗 Direktelenker:
- **Produktdata:** [product.json](http://127.0.0.1:9000/products/vw-volkswagen-id4-solbrilleholder/product.json)
- **Beskrivelse:** [description.md](http://127.0.0.1:9000/products/vw-volkswagen-id4-solbrilleholder/description.md)
- **Bilder:** [images/](http://127.0.0.1:9000/products/vw-volkswagen-id4-solbrilleholder/images/)
- **CAD-filer:** [cad-files/](http://127.0.0.1:9000/products/vw-volkswagen-id4-solbrilleholder/cad-files/)
- **Dokumentasjon:** [documentation/](http://127.0.0.1:9000/products/vw-volkswagen-id4-solbrilleholder/documentation/)

### 📊 MinIO Web Interface:
Tilgang til filer via MinIO web interface på:
`http://127.0.0.1:9000:9001`

**Mappe:** `products/vw-volkswagen-id4-solbrilleholder/`

### 🔄 Synkronisering:
- **GitHub → MinIO:** Referanser og metadata
- **MinIO → Shopify:** Produktdata og bilder synkroniseres automatisk
- **Last oppdatert:** 2025-09-11 19:45:25

## 💡 Redigering:
1. **Bilder/CAD-filer:** Last opp direkte til MinIO via web interface
2. **Produktdata:** Rediger JSON-filer i MinIO og kjør synkronisering
3. **Synkroniser til Shopify:** `python tools/sync_product_data.py --to-shopify --product vw-volkswagen-id4-solbrilleholder`
