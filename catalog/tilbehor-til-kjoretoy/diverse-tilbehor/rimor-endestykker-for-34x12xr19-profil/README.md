# Rimor endestykker for 34x12xR19 profil

**Handle:** `rimor-endestykker-for-34x12xr19-profil`  
**Status:** active  
**Leverandør:** Fladby 3Dprint

## 📁 Filstruktur (Lagret i MinIO)

Alle produktfiler er lagret i MinIO object storage og kan nås via:

### 🔗 Direktelenker:
- **Produktdata:** [product.json](http://127.0.0.1:9000/products/rimor-endestykker-for-34x12xr19-profil/product.json)
- **Beskrivelse:** [description.md](http://127.0.0.1:9000/products/rimor-endestykker-for-34x12xr19-profil/description.md)
- **Bilder:** [images/](http://127.0.0.1:9000/products/rimor-endestykker-for-34x12xr19-profil/images/)
- **CAD-filer:** [cad-files/](http://127.0.0.1:9000/products/rimor-endestykker-for-34x12xr19-profil/cad-files/)
- **Dokumentasjon:** [documentation/](http://127.0.0.1:9000/products/rimor-endestykker-for-34x12xr19-profil/documentation/)

### 📊 MinIO Web Interface:
Tilgang til filer via MinIO web interface på:
`http://127.0.0.1:9000:9001`

**Mappe:** `products/rimor-endestykker-for-34x12xr19-profil/`

### 🔄 Synkronisering:
- **GitHub → MinIO:** Referanser og metadata
- **MinIO → Shopify:** Produktdata og bilder synkroniseres automatisk
- **Last oppdatert:** 2025-09-11 19:45:25

## 💡 Redigering:
1. **Bilder/CAD-filer:** Last opp direkte til MinIO via web interface
2. **Produktdata:** Rediger JSON-filer i MinIO og kjør synkronisering
3. **Synkroniser til Shopify:** `python tools/sync_product_data.py --to-shopify --product rimor-endestykker-for-34x12xr19-profil`
