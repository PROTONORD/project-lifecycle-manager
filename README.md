# ProtoNord Wiki - Project Management and Workflow Overview

This is a Docusaurus-based wiki and project management platform for ProtoNord that keeps track of the entire workflow from idea to finished product. The system integrates file server content with Shopify products to provide complete traceability and status on all projects.

## 🎯 Main Features

  - **Project Overview**: Status on all projects (planned, in progress, completed)
  - **Shopify Integration**: Connects products in the store with design files and documentation
  - **File Server Connection**: Overview of CAD files, images, and documentation stored in the cloud
  - **Workflow Tracking**: From the first sketch to the published product in Shopify
  - **Dashboard**: Visual overview of the entire production pipeline

## 🌐 Live Websites

  - **Wiki and Dashboard**: [https://wiki.protonord.no](https://wiki.protonord.no)
  - **Repository**: [https://github.com/PROTONORD/project-lifecycle-manager](https://github.com/PROTONORD/project-lifecycle-manager)

## 🏗️ System Architecture

### Frontend (Docusaurus Wiki)

  - **Port**: 3001 (local development)
  - **Framework**: Docusaurus v3 with React components
  - **Content**:
      - Project documentation and workflow status
      - Shopify dashboard for product overview
      - File server integration and cloud backup documentation
      - Traceability from design files to finished product

### Project Management and Integrations

  - **Shopify API**: Dashboard showing products that are published in the store
  - **Cloud Storage**: Google Drive + Jottacloud for design files and documentation
  - **File Server Connection**: Overview of CAD files, images, and project files
  - **Status Tracking**: Which projects are planned, in progress, or completed
  - **Backup System**: GFS strategy with dual-cloud redundancy

### Infrastructure

  - **Web Server**: Apache with Let's Encrypt SSL
  - **Automation**: Cron-based scripts
  - **Version Control**: GitHub as the single source of truth

## 🚀 Getting Started

### 1\. Install dependencies

```bash
# Clone the project
git clone https://github.com/PROTONORD/project-lifecycle-manager.git
cd project-lifecycle-manager

# Install Node.js packages
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### 2\. Configure environment variables

```bash
# Copy the template and fill in your values
cp .env.template .env
```

Required variables:

```bash
# Shopify configuration
SHOPIFY_SHOP_URL=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_access_token
SHOPIFY_API_KEY=your_api_key
SHOPIFY_API_SECRET=your_api_secret

# Data configuration
DATA_ROOT=catalog
```

### 3\. Start the development server

```bash
# Start Docusaurus
npm start

# Or for production
npm run build
npm run serve
```

## 📁 Project Structure

```
project-lifecycle-manager/
├── docs/                     # Documentation (Markdown)
│   ├── backup-system.md      # Backup system guide
│   └── config-manager-guide.md # Config manager manual
├── src/                      # React components
│   ├── components/           # Reusable components
│   │   ├── ProtoNordHome.js  # Main page component
│   │   └── ShopifyDashboard.js # Shopify dashboard
│   └── pages/                # Docusaurus pages
├── static/                   # Static files
│   ├── data/shopify/         # Shopify JSON data
│   └── img/                  # Images and icons
├── scripts/                  # Automation scripts
│   ├── protonord_cloud_backup.sh   # Cloud backup system
│   ├── config_manager.sh         # Universal config manager
│   └── automated_protonord_sync.py # Shopify sync script
├── catalog/                  # Product catalog
└── data/                     # Local data files
```

## 🔄 Automation

### Cron Schedule

```bash
# Daily backup (01:30 AM)
30 1 * * * /path/to/protonord_cloud_backup.sh

# Shopify sync (02:00 AM)
0 2 * * * /path/to/automated_protonord_sync.py

# Docker backup (Sundays 03:00 AM)
0 3 * * 0 /path/to/backup_docker.sh
```

### Shopify Integration

  - **Project Status Dashboard**: Overview of which projects are published as products
  - **Product Linking**: Connects Shopify products with corresponding design files and documentation
  - **Workflow Tracking**: From the first CAD file to the finished product in the store
  - **Inventory Status**: Real-time overview of availability
  - **API Integration**: Secure access to Shopify data for project management
  - **Status Synchronization**: Automatic updates of project status based on Shopify data

### Cloud Backup System

  - **GFS Strategy**: Grandfather-Father-Son backup rotation
  - **Dual Cloud**: Google Drive + Jottacloud redundancy
  - **Automatic Cleanup**: Removes old backups
  - **Logging**: Detailed backup log

## 🛠️ Project Workflow

### Lifecycle: From Idea to Product

1.  **Planned** 📋

      - Idea is registered in the system
      - Design sketches and requirements are documented
      - Project folder is created in cloud storage

2.  **In Progress** 🛠️

      - CAD design and 3D modeling
      - Prototyping and testing
      - Files are synchronized to the file server
      - Documentation is updated continuously

3.  **Ready for Production** ✅

      - Design is finalized and validated
      - Product images and descriptions are ready
      - All files are organized in cloud storage

4.  **Published in Shopify** 🛒

      - Product is created in the Shopify store
      - Link between file server files and the Shopify product is established
      - Status is synchronized automatically

### File Server Integration

  - **CAD files**: `.step`, `.stl`, `.dwg` files in organized folders
  - **Product images**: High-resolution images for web and print
  - **Documentation**: README files with product information
  - **Status tracking**: Automatic detection of project status based on file structure

## 🛠️ Development Tools

### Config Manager

A universal tool for configuration management:

```bash
# Add a cron job
./scripts/config_manager.sh -b add crontab "0 2 * * * script.sh"

# Manage YAML/JSON files
./scripts/config_manager.sh -f config.yml add yaml "setting: value"

# Backup and restore
./scripts/config_manager.sh backup crontab
./scripts/config_manager.sh restore crontab backup_file.backup
```

### Backup System

```bash
# Manual backup
./scripts/protonord_cloud_backup.sh

# Check backup status
tail -f ~/protonord_backup.log

# Test cloud connection
rclone lsd gdrive:
rclone lsd jottacloud:
```

## 🎨 Frontend Features

### Dark Mode Support

  - Automatic theme detection
  - Responsive design for all screen sizes
  - Consistent styling across components

### Shopify Dashboard

  - Real-time product overview
  - Inventory statistics and trends
  - Order tracking
  - Interactive charts and graphs

### React Components

  - ProtoNordHome: Main page with product catalog
  - ShopifyDashboard: Admin dashboard
  - Responsive navigation and layout

## 🔐 Security

### API Security

  - Environment variables for sensitive data
  - Rate limiting on API calls
  - Secure webhook endpoints

### Backup Security

  - Encrypted cloud connections
  - Redundant storage on multiple services
  - Automatic integrity testing

### Access Control

  - GitHub-based access control
  - SSL/TLS for all web traffic
  - Secure cron job configuration

## 📊 Monitoring and Logging

### System Logs

```bash
# Backup logs
tail -f ~/protonord_backup.log

# Config manager logs
tail -f ~/config_manager.log

# Sync logs
tail -f logs/cron.log
```

### Performance Monitoring

  - Shopify API response times
  - Cloud upload statistics
  - Website load times
  - Error tracking and alerting

## 🚨 Troubleshooting

### Common Issues

#### Shopify API errors

```bash
# Test API connection
curl -H "X-Shopify-Access-Token: $TOKEN" https://shop.myshopify.com/admin/api/2023-10/products.json
```

#### Cloud backup problems

```bash
# Test rclone configuration
rclone config show
rclone lsd gdrive:
rclone lsd jottacloud:
```

#### Build/Deploy errors

```bash
# Clear cache and rebuild
npm run clear
npm install
npm run build
```

## 🔗 Related Projects

  - **Tromsoskapere Wiki**: [https://wiki.tromsoskapere.no](https://wiki.tromsoskapere.no)
  - **ProtoNord Shopify**: [https://protonord.myshopify.com](https://protonord.myshopify.com)

## 📚 Documentation

### API References

  - [Shopify Admin API](https://shopify.dev/api/admin)
  - [Docusaurus Documentation](https://docusaurus.io/)
  - [rclone Documentation](https://rclone.org/)

### Internal Guides

  - [Backup System Guide](https://www.google.com/search?q=docs/backup-system.md)
  - [Config Manager Manual](https://www.google.com/search?q=docs/config-manager-guide.md)

## 🤝 Contributing

1.  Fork the project
2.  Create a feature branch (`git checkout -b feature/new-feature`)
3.  Commit your changes (`git commit -m 'Add new feature'`)
4.  Push to the branch (`git push origin feature/new-feature`)
5.  Create a Pull Request

## 📝 License

This project is proprietary to ProtoNord AS.

-----

**Last updated**: September 2025
**Version**: 2.0
**Maintained by**: ProtoNord Development Team
