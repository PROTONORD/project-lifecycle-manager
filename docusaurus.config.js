// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const {themes} = require('prism-react-renderer');
const lightTheme = themes.github;
const darkTheme = themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Protonord Wiki',
  tagline: 'Project Management & Workflow Tracking System',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://wiki.protonord.no',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'PROTONORD', // Usually your GitHub org/user name.
  projectName: 'project-lifecycle-manager', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'no',
    locales: ['no', 'en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/PROTONORD/project-lifecycle-manager/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/protonord-social-card.jpg',
      navbar: {
        title: 'Protonord Wiki',
        logo: {
          alt: 'Protonord Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Dokumentasjon',
          },
          {to: '/cloud-files', label: '☁️ Cloud Files', position: 'left'},
          {to: '/shopify', label: '🛍️ Shopify', position: 'left'},
          {
            href: 'https://github.com/PROTONORD/project-lifecycle-manager',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Dokumentasjon',
            items: [
              {
                label: 'Hjem',
                to: '/',
              },
              {
                label: 'Cloud Storage',
                to: '/cloud-storage',
              },
            ],
          },
          {
            title: 'Samfunn',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/PROTONORD/project-lifecycle-manager',
              },
            ],
          },
          {
            title: 'Mer',
            items: [
              {
                label: 'Cloud Files',
                to: '/cloud-files',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Protonord. Bygget med Docusaurus.`,
      },
      prism: {
        theme: lightTheme,
        darkTheme: darkTheme,
      },
    }),
};

module.exports = config;