import React from 'react';
import ProtoNordHome from '@site/src/components/ProtoNordHome';
import Layout from '@theme/Layout';

export default function HomePage() {
  return (
    <Layout
      title="ProtoNord - Fra idé til virkelighet"
      description="Norsk 3D-printing og produktutvikling med fokus på kvalitet og bærekraft">
      <ProtoNordHome />
    </Layout>
  );
}