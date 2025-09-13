import React fr  },
  {
    title: '🔄 Automatisk Synkronisering',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        rclone og Shopify API holder data synkronisert og oppdatert automatisk
        med daglige scripts og sanntids cloud-oppdateringer.
      </>
    ),
  },
];;
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
    title: '🛍️ Shopify Integrering', 
    Svg: require('@site/static/img/protonord-logo.png').default,
    description: (
      <>
        Live dashboard med produkter, bestillinger og kunde-data fra ProtoNord Shopify butikken.
        Automatisk synkronisering hver natt for oppdatert business intelligence.
      </>
    ),
  },
    title: '�️ Shopify Integrering', 
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Live dashboard med produkter, bestillinger og kunde-data fra ProtoNord Shopify butikken.
        Automatisk synkronisering hver natt for oppdatert business intelligence.
      </>
    ),
  },
  {
    title: '� Automatisk Synkronisering',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        rclone og Shopify API holder data synkronisert og oppdatert automatisk
        med daglige scripts og sanntids cloud-oppdateringer.
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