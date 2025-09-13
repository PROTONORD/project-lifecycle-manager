# WeatherGuard for Netatmo utemodul

**Handle:** `weatherguard-for-netatmo-utemodul`  
**Status:** archived  
**Leverandør:** Fladby 3Dprint

## 📁 Filstruktur (Lagret i cloud backup)

Alle produktfiler er lagret i cloud backup repository og kan nås via:

### 🔗 Direktelenker:
- **Produktdata:** [product.json](http://127.0.0.1:9000/products/weatherguard-for-netatmo-utemodul/product.json)
- **Beskrivelse:** [description.md](http://127.0.0.1:9000/products/weatherguard-for-netatmo-utemodul/description.md)
- **Bilder:** [images/](http://127.0.0.1:9000/products/weatherguard-for-netatmo-utemodul/images/)
- **CAD-filer:** [cad-files/](http://127.0.0.1:9000/products/weatherguard-for-netatmo-utemodul/cad-files/)
- **Dokumentasjon:** [documentation/](http://127.0.0.1:9000/products/weatherguard-for-netatmo-utemodul/documentation/)

### 📊 cloud backup Web Interface:
Tilgang til filer via cloud backup web interface på:
`http://127.0.0.1:9000:9001`

**Mappe:** `products/weatherguard-for-netatmo-utemodul/`

### 🔄 Synkronisering:
- **GitHub → cloud backup:** Referanser og metadata
- **cloud backup → Shopify:** Produktdata og bilder synkroniseres automatisk
- **Last oppdatert:** 2025-09-11 19:45:26

## 💡 Redigering:
1. **Bilder/CAD-filer:** Last opp direkte til cloud backup via web interface
2. **Produktdata:** Rediger JSON-filer i cloud backup og kjør synkronisering
3. **Synkroniser til Shopify:** `python tools/sync_product_data.py --to-shopify --product weatherguard-for-netatmo-utemodul`
