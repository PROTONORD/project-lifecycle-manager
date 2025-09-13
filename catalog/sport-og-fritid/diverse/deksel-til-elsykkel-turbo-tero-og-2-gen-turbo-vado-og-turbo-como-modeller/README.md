# Deksel til Elsykkel Turbo Tero og 2.gen, Turbo Vado og Turbo Como modeller

**Handle:** `deksel-til-elsykkel-turbo-tero-og-2-gen-turbo-vado-og-turbo-como-modeller`  
**Status:** active  
**Leverandør:** PROTONORD

## 📁 Filstruktur (Lagret i MinIO)

Alle produktfiler er lagret i MinIO object storage og kan nås via:

### 🔗 Direktelenker:
- **Produktdata:** [product.json](http://127.0.0.1:9000/products/deksel-til-elsykkel-turbo-tero-og-2-gen-turbo-vado-og-turbo-como-modeller/product.json)
- **Beskrivelse:** [description.md](http://127.0.0.1:9000/products/deksel-til-elsykkel-turbo-tero-og-2-gen-turbo-vado-og-turbo-como-modeller/description.md)
- **Bilder:** [images/](http://127.0.0.1:9000/products/deksel-til-elsykkel-turbo-tero-og-2-gen-turbo-vado-og-turbo-como-modeller/images/)
- **CAD-filer:** [cad-files/](http://127.0.0.1:9000/products/deksel-til-elsykkel-turbo-tero-og-2-gen-turbo-vado-og-turbo-como-modeller/cad-files/)
- **Dokumentasjon:** [documentation/](http://127.0.0.1:9000/products/deksel-til-elsykkel-turbo-tero-og-2-gen-turbo-vado-og-turbo-como-modeller/documentation/)

### 📊 MinIO Web Interface:
Tilgang til filer via MinIO web interface på:
`http://127.0.0.1:9000:9001`

**Mappe:** `products/deksel-til-elsykkel-turbo-tero-og-2-gen-turbo-vado-og-turbo-como-modeller/`

### 🔄 Synkronisering:
- **GitHub → MinIO:** Referanser og metadata
- **MinIO → Shopify:** Produktdata og bilder synkroniseres automatisk
- **Last oppdatert:** 2025-09-11 19:45:25

## 💡 Redigering:
1. **Bilder/CAD-filer:** Last opp direkte til MinIO via web interface
2. **Produktdata:** Rediger JSON-filer i MinIO og kjør synkronisering
3. **Synkroniser til Shopify:** `python tools/sync_product_data.py --to-shopify --product deksel-til-elsykkel-turbo-tero-og-2-gen-turbo-vado-og-turbo-como-modeller`
