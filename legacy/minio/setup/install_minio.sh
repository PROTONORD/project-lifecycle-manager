#!/bin/bash
# Automatisk oppsett av MinIO server

set -e

echo "🚀 Setting up MinIO server..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Please run as root (use sudo)${NC}"
    exit 1
fi

# Download MinIO if not exists
if [ ! -f "/usr/local/bin/minio" ]; then
    echo "📥 Downloading MinIO..."
    wget -q https://dl.min.io/server/minio/release/linux-amd64/minio -O /tmp/minio
    chmod +x /tmp/minio
    mv /tmp/minio /usr/local/bin/
    echo -e "${GREEN}✅ MinIO binary installed${NC}"
else
    echo -e "${GREEN}✅ MinIO binary already exists${NC}"
fi

# Create minio user
if ! id "minio-user" &>/dev/null; then
    echo "👤 Creating minio-user..."
    useradd -r minio-user -s /sbin/nologin
    echo -e "${GREEN}✅ User minio-user created${NC}"
else
    echo -e "${GREEN}✅ User minio-user already exists${NC}"
fi

# Create data directory
DATA_DIR="/mnt/data"
if [ ! -d "$DATA_DIR" ]; then
    echo "📁 Creating data directory..."
    mkdir -p "$DATA_DIR"
    chown minio-user:minio-user "$DATA_DIR"
    echo -e "${GREEN}✅ Data directory created at $DATA_DIR${NC}"
else
    echo -e "${GREEN}✅ Data directory already exists${NC}"
    chown minio-user:minio-user "$DATA_DIR"
fi

# Copy configuration
echo "⚙️ Setting up configuration..."
cp setup/minio-config /etc/default/minio
chown root:root /etc/default/minio
chmod 640 /etc/default/minio
echo -e "${GREEN}✅ Configuration copied to /etc/default/minio${NC}"

# Install systemd service
echo "🔧 Installing systemd service..."
cp setup/minio.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable minio
echo -e "${GREEN}✅ Systemd service installed and enabled${NC}"

# Start MinIO
echo "▶️ Starting MinIO service..."
systemctl start minio

# Wait a moment for startup
sleep 3

# Check status
if systemctl is-active --quiet minio; then
    echo -e "${GREEN}✅ MinIO is running successfully!${NC}"
    
    # Show access information
    echo -e "\n${YELLOW}📋 Access Information:${NC}"
    echo "   Web Console: http://localhost:9001"
    echo "   API Endpoint: http://localhost:9000"
    echo "   Username: minioadmin"
    echo "   Password: minioadmin123"
    echo ""
    echo -e "${YELLOW}⚠️ SECURITY WARNING:${NC}"
    echo "   Change default credentials in /etc/default/minio"
    echo "   Restart service: sudo systemctl restart minio"
    echo ""
    echo -e "${GREEN}🎉 MinIO setup completed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Access web console and change credentials"
    echo "2. Create 'products' bucket"
    echo "3. Update .env file with correct credentials"
    echo "4. Run: python setup/validate_config.py"
    
else
    echo -e "${RED}❌ MinIO failed to start${NC}"
    echo "Check logs: sudo journalctl -u minio -f"
    exit 1
fi