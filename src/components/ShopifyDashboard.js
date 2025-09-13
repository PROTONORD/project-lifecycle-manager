import React, { useState, useEffect } from 'react';
import styles from './ShopifyDashboard.module.css';

const ShopifyDashboard = () => {
  const [shopifyData, setShopifyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [showAllProducts, setShowAllProducts] = useState(true);
  const [productFilter, setProductFilter] = useState('all'); // 'all', 'available', 'unavailable'
  const [selectedImages, setSelectedImages] = useState({}); // Nytt state for bildegalleri

  useEffect(() => {
    fetchShopifyData();
  }, []);

  const fetchShopifyData = async () => {
    try {
      // Hent data fra offentlig JSON uten sensitive data
      const response = await fetch('/data/shopify/protonord_shopify_public.json');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setShopifyData(data);
    } catch (err) {
      console.error('Feil ved henting av Shopify data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('nb-NO');
  };

  // Funksjon for å generere Shopify butikk URLs
  const getShopifyUrls = (product) => {
    const baseUrl = 'https://protonord.no';
    const productHandle = product.handle; // Shopify slug for produktet
    
    return {
      product: `${baseUrl}/products/${productHandle}`,
      // Prøv å finne kolleksjon basert på product_type
      collection: product.product_type ? `${baseUrl}/collections/${encodeURIComponent(product.product_type.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, ''))}` : null,
      // Alternativ: Direkte til alle produkter
      allProducts: `${baseUrl}/collections/all`
    };
  };

  const handleImageChange = (productId, imageIndex) => {
    setSelectedImages(prev => ({
      ...prev,
      [productId]: imageIndex
    }));
  };

  if (loading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
        <p>Laster Shopify data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.error}>
        <h3>❌ Kunne ikke laste Shopify data</h3>
        <p>{error}</p>
        <button onClick={fetchShopifyData} className={styles.retryButton}>
          🔄 Prøv igjen
        </button>
      </div>
    );
  }

  if (!shopifyData) {
    return (
      <div className={styles.noData}>
        <h3>📭 Ingen Shopify data tilgjengelig</h3>
        <p>Data synkroniseres automatisk hver natt</p>
        <button onClick={fetchShopifyData} className={styles.retryButton}>
          🔄 Last inn data
        </button>
      </div>
    );
  }

  const { shop_info, statistics, last_updated } = shopifyData;
  
  // Filtrer ut 3dscanning-produkter og arkiverte produkter for statistikk og visning
  const filteredProducts = shopifyData.products?.filter(product => 
    !product.title.toLowerCase().includes('3dscanning') &&
    !product.title.toLowerCase().includes('3d scanning') &&
    !product.title.toLowerCase().includes('scanning') &&
    product.status !== 'archived'  // Ekskluder arkiverte produkter
  ) || [];
  
  // Opprett justerte statistikker uten 3dscanning-produkter
  const adjustedStatistics = {
    ...statistics,
    products: filteredProducts.length
  };

  const renderOverview = () => (
    <div className={styles.overview}>
      <div className={styles.shopInfo}>
        <h3>🏪 {shop_info.name}</h3>
        <p><strong>Domene:</strong> {shop_info.domain}</p>
        <p><strong>Land:</strong> {shop_info.country_name}</p>
        <p><strong>Valuta:</strong> {shop_info.currency}</p>
        <p><strong>Sist synkronisert:</strong> {formatDate(last_updated)}</p>
      </div>

      <div className={styles.statsGrid}>
        <div className={styles.statCard}>
          <div className={styles.statIcon}>📦</div>
          <div className={styles.statContent}>
            <h4>Produkter</h4>
            <span className={styles.statNumber}>{adjustedStatistics.products}</span>
          </div>
        </div>

        <div className={styles.statCard}>
          <div className={styles.statIcon}>🛒</div>
          <div className={styles.statContent}>
            <h4>Bestillinger</h4>
            <span className={styles.statNumber}>{statistics.orders}</span>
            <small>Siste 30 dager</small>
          </div>
        </div>

        <div className={styles.statCard}>
          <div className={styles.statIcon}>👥</div>
          <div className={styles.statContent}>
            <h4>Kunder</h4>
            <span className={styles.statNumber}>{statistics.customers}</span>
            <small>Siste 90 dager</small>
          </div>
        </div>

        <div className={styles.statCard}>
          <div className={styles.statIcon}>📁</div>
          <div className={styles.statContent}>
            <h4>Kolleksjoner</h4>
            <span className={styles.statNumber}>
              {statistics.smart_collections + statistics.custom_collections}
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderProducts = () => {
    const displayProducts = showAllProducts 
      ? filteredProducts 
      : filteredProducts?.slice(0, 12);
    
    // Lag inventory lookup map (fallback til variant inventory hvis inventory_levels ikke finnes)
    const inventoryMap = {};
    if (shopifyData.inventory_levels && Array.isArray(shopifyData.inventory_levels)) {
      shopifyData.inventory_levels.forEach(level => {
        inventoryMap[level.inventory_item_id] = level.available;
      });
    }
    
    // Hjelpefunksjon for å få riktig inventory
    const getProductInventory = (product) => {
      const variant = product.variants?.[0];
      if (!variant) return 0;
      
      // Prøv først inventory_levels API data
      const inventoryFromAPI = inventoryMap[variant.inventory_item_id];
      if (inventoryFromAPI !== undefined && inventoryFromAPI !== null) {
        return inventoryFromAPI;
      }
      
      // Fall tilbake til variant inventory_quantity
      return variant.inventory_quantity || 0;
    };
    
    // Lag collection lookup map  
    const productCollections = {};
    if (shopifyData.collections?.custom_collections) {
      shopifyData.collections.custom_collections.forEach(collection => {
        if (collection.product_ids) {
          collection.product_ids.forEach(productId => {
            if (!productCollections[productId]) {
              productCollections[productId] = [];
            }
            productCollections[productId].push(collection.title);
          });
        }
      });
    }

    // Separer og sorter produkter basert på tilgjengelighet for kjøp
    const availableProducts = [];
    const unavailableProducts = [];

    displayProducts?.forEach(product => {
      const inventory = getProductInventory(product);
      const price = parseFloat(product.variants?.[0]?.price || 0);
      
      // Produkter regnes som under utvikling hvis:
      // 1. Lager er under 10 stk (inkludert 0)
      // 2. Pris er 0,-
      if (inventory < 10 || price === 0) {
        unavailableProducts.push(product);
      } else {
        availableProducts.push(product);
      }
    });

    // Filtrer produkter basert på valgt filter
    let sortedProducts = [];
    if (productFilter === 'available') {
      sortedProducts = availableProducts;
    } else if (productFilter === 'unavailable') {
      sortedProducts = unavailableProducts;
    } else {
      // 'all' - vis alle produkter: tilgjengelige først, deretter utilgjengelige
      sortedProducts = [...availableProducts, ...unavailableProducts];
    }

    const renderProductCard = (product) => {
      const variant = product.variants?.[0];
      const inventory = getProductInventory(product);
      const collections = productCollections[product.id] || [];
      const images = product.images || [];
      const hasMultipleImages = images.length > 1;
      const currentImageIndex = selectedImages[product.id] || 0;
      const shopifyUrls = getShopifyUrls(product);
      const isUnavailable = inventory === 0;
      
      return (
        <div key={product.id} className={`${styles.productCard} ${isUnavailable ? styles.unavailableProduct : ''}`}>
          {isUnavailable && (
            <div className={styles.unavailableLabel}>
              � Utilgjengelig
            </div>
          )}
          <div className={styles.productImageContainer}>
            {images[currentImageIndex] && (
              <a 
                href={shopifyUrls.product} 
                target="_blank" 
                rel="noopener noreferrer"
                className={styles.productImageLink}
              >
                <img 
                  src={images[currentImageIndex].src} 
                  alt={product.title}
                  className={styles.productImage}
                />
              </a>
            )}
            {hasMultipleImages && (
              <>
                <div className={styles.imageGallery}>
                  <div className={styles.imageCount}>
                    📷 {currentImageIndex + 1}/{images.length}
                  </div>
                </div>
                <div className={styles.imageControls}>
                  <button 
                    className={styles.imageBtn}
                    onClick={() => handleImageChange(product.id, Math.max(0, currentImageIndex - 1))}
                    disabled={currentImageIndex === 0}
                  >
                    ←
                  </button>
                  <button 
                    className={styles.imageBtn}
                    onClick={() => handleImageChange(product.id, Math.min(images.length - 1, currentImageIndex + 1))}
                    disabled={currentImageIndex === images.length - 1}
                  >
                    →
                  </button>
                </div>
              </>
            )}
          </div>
          
          <div className={styles.productInfo}>
            <h4>
              <a 
                href={shopifyUrls.product} 
                target="_blank" 
                rel="noopener noreferrer"
                className={styles.productTitleLink}
              >
                {product.title}
              </a>
            </h4>
            
            <div className={styles.productDetails}>
              {product.product_type && (
                <p>
                  <strong>Kategori:</strong> 
                  <a 
                    href={shopifyUrls.collection || shopifyUrls.allProducts} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className={styles.categoryLink}
                  >
                    {product.product_type}
                  </a>
                </p>
              )}
              
              {product.vendor && (
                <p><strong>Leverandør:</strong> {product.vendor}</p>
              )}
              
              {collections.length > 0 && (
                <p><strong>Menyer:</strong> {collections.slice(0, 2).join(', ')}{collections.length > 2 ? '...' : ''}</p>
              )}
              
              {variant && (
                <>
                  <p className={styles.productPrice}>
                    <strong>Pris:</strong> {variant.price} NOK
                  </p>
                  
                  {variant.weight && (
                    <p><strong>Vekt:</strong> {variant.weight} {variant.weight_unit}</p>
                  )}
                  
                  {variant.sku && (
                    <p><strong>SKU:</strong> {variant.sku}</p>
                  )}
                  
                  {product.variants.length > 1 && (
                    <div>
                      <p><strong>Varianter ({product.variants.length} stk):</strong></p>
                      <div className={styles.variantsList}>
                        {product.variants.map((variant, index) => (
                          <div key={variant.id} className={styles.variantItem}>
                            <span className={styles.variantTitle}>{variant.title}</span>
                            {variant.price && parseFloat(variant.price) > 0 && (
                              <span className={styles.variantPrice}>{variant.price} kr</span>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              )}
              
              {product.tags && (
                <p><strong>Tags:</strong> {product.tags.split(',').slice(0, 3).join(', ')}</p>
              )}
            </div>
            
            <div className={styles.productActions}>
              <a 
                href={shopifyUrls.product} 
                target="_blank" 
                rel="noopener noreferrer"
                className={styles.shopLink}
              >
                🛍️ Se i butikk
              </a>
            </div>
            
            <span className={styles.productStatus}>
              {product.status === 'active' ? '✅ Aktiv' : '⏸️ Inaktiv'}
            </span>
          </div>
        </div>
      );
    };
    
    return (
      <div className={styles.products}>
        <h3>📦 Produkter ({adjustedStatistics.products})</h3>
        <div className={styles.productStats}>
          <span className={styles.productStat}>✅ {availableProducts.length} tilgjengelig for kjøp</span>
          <span className={styles.productStat}>� {unavailableProducts.length} utilgjengelig (under utvikling)</span>
        </div>
        
        <div className={styles.productGrid}>
          {sortedProducts.map(renderProductCard)}
        </div>
        
        {filteredProducts?.length > 12 && (
          <div className={styles.showMoreContainer}>
            <button 
              onClick={() => setShowAllProducts(!showAllProducts)}
              className={styles.showMoreButton}
            >
              {showAllProducts 
                ? `↑ Vis færre (12 produkter)` 
                : `↓ Vis alle ${filteredProducts.length} produkter`
              }
            </button>
            <p className={styles.showingCount}>
              Viser {displayProducts?.length} av {filteredProducts.length} produkter
            </p>
          </div>
        )}
      </div>
    );
  };

  const renderOrders = () => (
    <div className={styles.orders}>
      <h3>🛒 Bestillinger ({statistics.orders})</h3>
      <div className={styles.ordersList}>
        {shopifyData.orders?.slice(0, 10).map(order => (
          <div key={order.id} className={styles.orderCard}>
            <div className={styles.orderHeader}>
              <span className={styles.orderNumber}>Bestilling #{order.order_number}</span>
              <span className={styles.orderDate}>{formatDate(order.created_at)}</span>
            </div>
            <div className={styles.orderDetails}>
              <p><strong>Antall produkter:</strong> {order.line_items_count || order.line_items?.length || 0}</p>
              <p><strong>Status:</strong> 
                <span className={`${styles.orderStatus} ${styles[order.financial_status]}`}>
                  {order.financial_status}
                </span>
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderCollections = () => {
    // Tell hvor mange kolleksjoner som faktisk har produkter
    const collectionsWithProducts = shopifyData.collections?.custom_collections?.filter(collection => collection.products_count > 0) || [];
    
    // Bygg trestruktur basert på produktdata
    const buildTreeStructure = () => {
      const tree = {};
      
      shopifyData.products.forEach(product => {
        const type = product.product_type || 'Diverse';
        const vendor = product.vendor || 'Ukjent leverandør';
        
        // Hovedkategori (product_type)
        if (!tree[type]) {
          tree[type] = {
            count: 0,
            vendors: {},
            brands: {},
            total: 0
          };
        }
        
        // Leverandør under kategorien
        if (!tree[type].vendors[vendor]) {
          tree[type].vendors[vendor] = {
            count: 0,
            brands: {},
            products: []
          };
        }
        
        tree[type].vendors[vendor].count++;
        tree[type].vendors[vendor].products.push(product);
        tree[type].total++;
        
        // Hvis det er bilrelatert, legg til bilmerker
        if (type === 'Tilbehør til kjøretøy' && product.tags) {
          const tags = product.tags.split(', ');
          const carBrands = ['Audi', 'Mercedes', 'BMW', 'Volvo', 'Toyota', 'Ford', 'Volkswagen', 'Peugeot', 'Citroen', 'Hyundai', 'Kia', 'Skoda', 'BYD', 'Tesla', 'Porsche', 'Lexus', 'MG4', 'Polestar'];
          
          tags.forEach(tag => {
            const brand = carBrands.find(b => tag.includes(b));
            if (brand) {
              if (!tree[type].brands[brand]) {
                tree[type].brands[brand] = [];
              }
              tree[type].brands[brand].push(product);
              
              if (!tree[type].vendors[vendor].brands[brand]) {
                tree[type].vendors[vendor].brands[brand] = [];
              }
              tree[type].vendors[vendor].brands[brand].push(product);
            }
          });
        }
      });
      
      return tree;
    };

    const treeStructure = buildTreeStructure();
    
    return (
      <div className={styles.collections}>
        <h3>📁 Produktkategorier & Trestruktur</h3>
        
        {/* Trestruktur-visning */}
        <div className={styles.treeSection}>
          <h4>🌲 Kategorier og leverandører</h4>
          <div className={styles.treeContainer}>
            {Object.entries(treeStructure)
              .sort((a, b) => b[1].total - a[1].total)
              .map(([category, data]) => (
                <div key={category} className={styles.treeNode}>
                  <div className={styles.treeNodeHeader}>
                    <span className={styles.treeIcon}>📂</span>
                    <a 
                      href={`https://protonord.no/collections/${encodeURIComponent(category.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, ''))}`}
                      target="_blank" 
                      rel="noopener noreferrer"
                      className={styles.treeCategoryLink}
                    >
                      <strong>{category}</strong>
                    </a>
                    <span className={styles.nodeCount}>({data.total} produkter)</span>
                  </div>
                  
                  {/* Leverandører under kategori */}
                  <div className={styles.treeChildren}>
                    {Object.entries(data.vendors)
                      .sort((a, b) => b[1].count - a[1].count)
                      .map(([vendor, vendorData]) => (
                        <div key={vendor} className={styles.treeSubNode}>
                          <div className={styles.treeSubNodeHeader}>
                            <span className={styles.treeIcon}>├─ 🏢</span>
                            <span>{vendor}</span>
                            <span className={styles.nodeCount}>({vendorData.count} produkter)</span>
                          </div>
                          
                          {/* Bilmerker hvis relevant */}
                          {Object.keys(vendorData.brands).length > 0 && (
                            <div className={styles.treeSubChildren}>
                              {Object.entries(vendorData.brands)
                                .sort((a, b) => b[1].length - a[1].length)
                                .map(([brand, products]) => (
                                  <div key={brand} className={styles.treeLeaf}>
                                    <span className={styles.treeIcon}>│  ├─ 🚗</span>
                                    <span>{brand}</span>
                                    <span className={styles.nodeCount}>({products.length} produkter)</span>
                                  </div>
                                ))}
                            </div>
                          )}
                        </div>
                      ))}
                  </div>
                </div>
              ))}
          </div>
        </div>
        
        {/* Viser faktiske Shopify kolleksjoner hvis noen har produkter */}
        {collectionsWithProducts.length > 0 && (
          <div className={styles.collectionSection}>
            <h4>�️ Shopify Kolleksjoner ({collectionsWithProducts.length})</h4>
            <div className={styles.collectionGrid}>
              {collectionsWithProducts.slice(0, 10).map(collection => (
                <div key={collection.id} className={styles.collectionCard}>
                  <h5>{collection.title}</h5>
                  <p><strong>Produkter:</strong> {collection.products_count || 0}</p>
                  {collection.body_html && (
                    <p className={styles.collectionDescription}>
                      {collection.body_html.replace(/<[^>]*>/g, '').substring(0, 100)}...
                    </p>
                  )}
                  <span className={`${styles.collectionStatus} ${collection.published_at ? styles.published : styles.draft}`}>
                    {collection.published_at ? '🟢 Publisert' : '🟡 Utkast'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className={styles.shopifyDashboard}>
      <div className={styles.header}>
        <h2>🛍️ ProtoNord Shopify Dashboard</h2>
        <p>Live data fra Shopify butikken</p>
      </div>

      <div className={styles.tabs}>
        <button 
          className={`${styles.tab} ${activeTab === 'overview' ? styles.active : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Oversikt
        </button>
        <button 
          className={`${styles.tab} ${activeTab === 'products' ? styles.active : ''}`}
          onClick={() => setActiveTab('products')}
        >
          📦 Produkter
        </button>
        <button 
          className={`${styles.tab} ${activeTab === 'orders' ? styles.active : ''}`}
          onClick={() => setActiveTab('orders')}
        >
          🛒 Bestillinger
        </button>
        <button 
          className={`${styles.tab} ${activeTab === 'collections' ? styles.active : ''}`}
          onClick={() => setActiveTab('collections')}
        >
          📁 Kolleksjoner
        </button>
      </div>

      <div className={styles.tabContent}>
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'products' && renderProducts()}
        {activeTab === 'orders' && renderOrders()}
        {activeTab === 'collections' && renderCollections()}
      </div>

      <div className={styles.footer}>
        <p>
          <strong>Datasynkronisering:</strong> Shopify data synkroniseres automatisk hver natt kl 02:00
        </p>
        <p>
          <strong>Sist oppdatert:</strong> {new Date(last_updated).toLocaleString('nb-NO')}
        </p>
      </div>
    </div>
  );
};

export default ShopifyDashboard;