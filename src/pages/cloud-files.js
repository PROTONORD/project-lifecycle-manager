import React from 'react';
import Layout from '@theme/Layout';
import CloudFileExplorer from '../components/CloudFileExplorer';

export default function CloudFiles() {
  return (
    <Layout
      title="Cloud Files"
      description="Utforsk filer lagret i ProtoNord cloud-tjenester">
      <main>
        <div className="container margin-vert--lg">
          <CloudFileExplorer />
        </div>
      </main>
    </Layout>
  );
}