#!/bin/bash

# Script for å fjerne gjenværende MinIO-referanser
WORKSPACE_ROOT="/home/kau005/prototype-workflow-med-github"

echo "🧹 Cleaning remaining MinIO references..."

# Clean JSON files - replace minio_location with cloud_location
echo "📝 Updating product_reference.json files..."
find "$WORKSPACE_ROOT/catalog" -name "product_reference.json" -exec sed -i 's/"minio_location"/"cloud_location"/g' {} \;

# Clean .gitkeep files
echo "📁 Updating .gitkeep files..."
find "$WORKSPACE_ROOT/catalog" -name ".gitkeep" -exec sed -i 's/MinIO/cloud backup/g' {} \;

# Clean FILES.md files
echo "📄 Updating FILES.md files..."
find "$WORKSPACE_ROOT/catalog" -name "FILES.md" -exec sed -i 's/MinIO/cloud backup/g' {} \;
find "$WORKSPACE_ROOT/catalog" -name "FILES.md" -exec sed -i 's/minio/cloud backup/g' {} \;

# Clean main.py
echo "🐍 Updating main.py..."
sed -i 's/Shopify-MinIO-GitHub/Shopify-Cloud-GitHub/g' "$WORKSPACE_ROOT/main.py"
sed -i 's/MinIO bucket/cloud bucket/g' "$WORKSPACE_ROOT/main.py"

# Clean catalog_summary.json
echo "📊 Updating catalog_summary.json..."
sed -i 's/"minio_bucket"/"cloud_bucket"/g' "$WORKSPACE_ROOT/catalog/catalog_summary.json"

# Clean .gitignore
echo "🙈 Updating .gitignore..."
sed -i 's/# MinIO data/# Cloud storage data/g' "$WORKSPACE_ROOT/.gitignore"
sed -i 's/minio-data/cloud-data/g' "$WORKSPACE_ROOT/.gitignore"

echo "✅ Cleanup completed!"
echo "📈 Summary of changes:"
echo "   - JSON files: minio_location → cloud_location"
echo "   - Documentation: MinIO → cloud backup"
echo "   - System references updated"