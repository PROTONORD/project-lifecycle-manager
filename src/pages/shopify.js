import React from 'react';
import Layout from '@theme/Layout';
import ShopifyDashboard from '@site/src/components/ShopifyDashboard';

export default function ShopifyPage() {
  return (
    <Layout
      title="Shopify Dashboard"
      description="Live data fra ProtoNord Shopify butikk">
      <main>
        <div className="container">
          <ShopifyDashboard />
        </div>
      </main>
    </Layout>
  );
}