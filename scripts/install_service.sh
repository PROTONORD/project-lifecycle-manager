#!/bin/bash

# Script for å installere Project Lifecycle Manager som systemd service
# Dette gjør at serveren starter automatisk ved server restart

echo "🔧 Installerer Project Lifecycle Manager som systemd service..."

# Kopier service fil til systemd
sudo cp /home/kau005/project-lifecycle-manager/project-lifecycle-manager.service /etc/systemd/system/

# Reload systemd og aktiver service
sudo systemctl daemon-reload
sudo systemctl enable project-lifecycle-manager.service

echo "✅ Service installert og aktivert!"
echo ""
echo "📋 Kommandoer for å administrere service:"
echo "   sudo systemctl start project-lifecycle-manager    # Start service"
echo "   sudo systemctl stop project-lifecycle-manager     # Stopp service"
echo "   sudo systemctl restart project-lifecycle-manager  # Restart service"
echo "   sudo systemctl status project-lifecycle-manager   # Sjekk status"
echo "   sudo journalctl -u project-lifecycle-manager -f   # Se logger"
echo ""
echo "🚀 Serveren vil nå starte automatisk ved system restart!"