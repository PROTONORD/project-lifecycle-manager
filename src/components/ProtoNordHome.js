import React, { useState, useEffect } from 'react';
import styles from './ProtoNordHome.module.css';

const ProtoNordHome = () => {
  const [shopifyData, setShopifyData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchShopifyData();
  }, []);

  const fetchShopifyData = async () => {
    try {
      const response = await fetch('/data/shopify/protonord_shopify_public.json');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      setShopifyData(data);
    } catch (err) {
      console.error('Feil ved henting av Shopify data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
        <p>Laster ProtoNord data...</p>
      </div>
    );
  }

  const { shop_info, statistics, products } = shopifyData || {};
  const featuredProducts = products?.slice(0, 6) || [];
  const categories = shopifyData?.collections?.custom_collections?.slice(0, 8) || [];

  return (
    <div className={styles.protonordHome}>
      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>PROTONORD</h1>
          <p className={styles.heroSubtitle}>Fra idé til virkelighet med vår ekspertise</p>
          <div className={styles.heroFeatures}>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>🇳🇴</div>
              <h3>Ekte norsk produksjon</h3>
              <p>Våre produkter blir skreddersydd for deg og produsert i Norge</p>
            </div>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>⚡</div>
              <h3>Rask levering</h3>
              <p>Sender normalt varene innen 1-5 virkedager</p>
            </div>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>🔧</div>
              <h3>Skreddersydde løsninger</h3>
              <p>3D-skanning og tilpasset design for dine behov</p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className={styles.stats}>
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <div className={styles.statNumber}>{statistics?.products || 0}</div>
            <div className={styles.statLabel}>Produkter</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statNumber}>{statistics?.custom_collections || 0}</div>
            <div className={styles.statLabel}>Kategorier</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statNumber}>{statistics?.orders || 0}</div>
            <div className={styles.statLabel}>Bestillinger</div>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className={styles.featuredProducts}>
        <h2>Våre nyeste produkter</h2>
        <div className={styles.productGrid}>
          {featuredProducts.map(product => (
            <div key={product.id} className={styles.productCard}>
              {product.images?.[0] && (
                <div className={styles.productImageContainer}>
                  <img 
                    src={product.images[0].src} 
                    alt={product.title}
                    className={styles.productImage}
                  />
                  {product.images.length > 1 && (
                    <div className={styles.imageCount}>📷 {product.images.length}</div>
                  )}
                </div>
              )}
              <div className={styles.productInfo}>
                <h3>{product.title}</h3>
                <p className={styles.productCategory}>{product.product_type}</p>
                {product.variants?.[0] && (
                  <p className={styles.productPrice}>{product.variants[0].price} NOK</p>
                )}
                <span className={`${styles.productStatus} ${product.status === 'active' ? styles.active : styles.inactive}`}>
                  {product.status === 'active' ? 'På lager' : 'Ikke tilgjengelig'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Services Section */}
      <section className={styles.services}>
        <h2>Våre tjenester</h2>
        <div className={styles.servicesGrid}>
          <div className={styles.serviceCard}>
            <div className={styles.serviceIcon}>🔍</div>
            <h3>3D-skanning av bilmodeller</h3>
            <p>Vi tilbyr 3D-skanning av bilmodeller vi ikke har på lager. Velg mellom alle store bilmerker og få skannet din bilmodell.</p>
            <a 
              href="https://protonord.myshopify.com/products/3dscanning-av-bilmodell-vi-ikke-har" 
              target="_blank" 
              rel="noopener noreferrer"
              className={styles.serviceButton}
            >
              Se alle bilmerker →
            </a>
          </div>
          <div className={styles.serviceCard}>
            <div className={styles.serviceIcon}>⚙️</div>
            <h3>Innovativt redesign</h3>
            <p>Vi kan til og med forbedre designet for å forhindre at de går i stykker på samme sted som originalen.</p>
          </div>
          <div className={styles.serviceCard}>
            <div className={styles.serviceIcon}>�🇴</div>
            <h3>Lokalproduksjon</h3>
            <p>Norskproduserte løsninger med fokus på kvalitet, bærekraft og lokal verdiskapning.</p>
          </div>
        </div>
      </section>

      {/* Development Process */}
      <section className={styles.process}>
        <h2>Vår utviklingsprosess</h2>
        <div className={styles.processGrid}>
          <div className={styles.processStep}>
            <div className={styles.stepNumber}>1</div>
            <h3>3D Scannet</h3>
            <p>Produkter som er 3D-scannet og klar for designfase</p>
          </div>
          <div className={styles.processStep}>
            <div className={styles.stepNumber}>2</div>
            <h3>Designfase</h3>
            <p>Produkter under utvikling etter 3D-skanning</p>
          </div>
          <div className={styles.processStep}>
            <div className={styles.stepNumber}>3</div>
            <h3>Betatesting</h3>
            <p>Siste fase før produksjon hvor vi trenger testing</p>
          </div>
          <div className={styles.processStep}>
            <div className={styles.stepNumber}>4</div>
            <h3>Produksjon</h3>
            <p>Ferdig testet og klar for salg</p>
          </div>
        </div>
      </section>

      {/* Footer Info */}
      <section className={styles.footer}>
        <div className={styles.footerContent}>
          <div className={styles.footerInfo}>
            <h3>Om ProtoNord</h3>
            <p>
              Vi tilbyr 3D-skanning og spesialdesignet produksjon med fokus på kvalitet som gjør våre kunder fornøyde. 
              Vår erfaring viser at kundene våre ønsker produkter som er holdbare og bærekraftige.
            </p>
          </div>
          <div className={styles.footerLinks}>
            <h3>Følg oss</h3>
            <div className={styles.socialLinks}>
              <span>📘 Facebook</span>
              <span>📷 Instagram</span>
              <span>📺 YouTube</span>
            </div>
          </div>
        </div>
        <div className={styles.footerBottom}>
          <p>© 2025, PROTONORD - Norsk kvalitet og innovasjon</p>
          <p>Sist oppdatert: {shopifyData?.last_updated ? new Date(shopifyData.last_updated).toLocaleDateString('nb-NO') : ''}</p>
        </div>
      </section>
    </div>
  );
};

export default ProtoNordHome;