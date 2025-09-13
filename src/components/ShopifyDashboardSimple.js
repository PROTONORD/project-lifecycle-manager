import React, { useState, useEffect } from 'react';
import styles from './ShopifyDashboard.module.css';

const ShopifyDashboardSimple = () => {
  const [shopifyData, setShopifyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchShopifyData();
  }, []);

  const fetchShopifyData = async () => {
    try {
      console.log('Fetching Shopify data...');
      const response = await fetch('/data/shopify/protonord_shopify_public.json');
      console.log('Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Data loaded:', data);
      setShopifyData(data);
    } catch (err) {
      console.error('Error fetching Shopify data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.shopifyDashboard}>
        <div className={styles.header}>
          <h2>🛍️ ProtoNord Shopify Dashboard</h2>
          <p>Live data fra Shopify butikken</p>
        </div>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Laster Shopify data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.shopifyDashboard}>
        <div className={styles.header}>
          <h2>🛍️ ProtoNord Shopify Dashboard</h2>
          <p>Live data fra Shopify butikken</p>
        </div>
        <div className={styles.error}>
          <h3>❌ Kunne ikke laste Shopify data</h3>
          <p>{error}</p>
          <button onClick={fetchShopifyData} className={styles.retryButton}>
            🔄 Prøv igjen
          </button>
        </div>
      </div>
    );
  }

  if (!shopifyData) {
    return (
      <div className={styles.shopifyDashboard}>
        <div className={styles.header}>
          <h2>🛍️ ProtoNord Shopify Dashboard</h2>
          <p>Live data fra Shopify butikken</p>
        </div>
        <div className={styles.noData}>
          <h3>📭 Ingen Shopify data tilgjengelig</h3>
          <p>Data synkroniseres automatisk hver natt</p>
          <button onClick={fetchShopifyData} className={styles.retryButton}>
            🔄 Last inn data
          </button>
        </div>
      </div>
    );
  }

  const { shop_info, statistics, last_updated } = shopifyData;

  return (
    <div className={styles.shopifyDashboard}>
      <div className={styles.header}>
        <h2>🛍️ ProtoNord Shopify Dashboard</h2>
        <p>Live data fra Shopify butikken</p>
      </div>

      <div className={styles.overview}>
        <div className={styles.shopInfo}>
          <h3>🏪 {shop_info?.name || 'Ukjent butikk'}</h3>
          <p><strong>Domene:</strong> {shop_info?.domain || 'Ukjent'}</p>
          <p><strong>Land:</strong> {shop_info?.country_name || 'Ukjent'}</p>
          <p><strong>Produkter:</strong> {statistics?.products || 0}</p>
          <p><strong>Bestillinger:</strong> {statistics?.orders || 0}</p>
          <p><strong>Kunder:</strong> {statistics?.customers || 0}</p>
        </div>
      </div>

      <div className={styles.footer}>
        <p>
          <strong>Sist oppdatert:</strong> {last_updated ? new Date(last_updated).toLocaleString('nb-NO') : 'Ukjent'}
        </p>
      </div>
    </div>
  );
};

export default ShopifyDashboardSimple;