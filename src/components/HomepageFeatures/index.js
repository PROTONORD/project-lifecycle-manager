import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: '☁️ Cloud Storage Oversikt',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Få fullstendig oversikt over alle ProtoNord-filer lagret i Jottacloud og Google Drive
        med automatisk katalogisering og søkefunksjonalitet.
      </>
    ),
  },
  {
    title: '🔄 Automatisk Synkronisering', 
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        rclone holder dine cloud storage tjenester synkronisert og oppdatert
        fra protonord-mappene med automatiske scripts og sanntidsoppdateringer.
      </>
    ),
  },
  {
    title: '📚 Dokumentasjon som Kode',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        All dokumentasjon lagres i Git og bygges automatisk med Docusaurus.
        Enkelt å vedlikeholde og dele med teamet.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}