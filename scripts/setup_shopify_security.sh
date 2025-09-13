#!/bin/bash
# ProtoNord Shopify Setup Script
# Sikker konfigurasjon av API-nøkler

SCRIPT_DIR="/home/kau005/project-lifecycle-manager"
ENV_FILE="$SCRIPT_DIR/.env"
TEMPLATE_FILE="$SCRIPT_DIR/.env.template"

echo "🔐 ProtoNord Shopify API Setup"
echo "================================"

# Sjekk om .env allerede eksisterer
if [ -f "$ENV_FILE" ]; then
    echo "⚠️ .env fil eksisterer allerede!"
    echo "Innhold (uten sensitive verdier):"
    grep -E "^[A-Z_]+=.*" "$ENV_FILE" | sed 's/=.*/=***SKJULT***/'
    echo ""
    read -p "Vil du oppdatere eksisterende .env fil? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Avbryter..."
        exit 1
    fi
fi

# Sjekk at template eksisterer
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "❌ Template fil ikke funnet: $TEMPLATE_FILE"
    exit 1
fi

echo "📝 Opprett/oppdater .env fil fra template..."

# Kopier template hvis .env ikke eksisterer
if [ ! -f "$ENV_FILE" ]; then
    cp "$TEMPLATE_FILE" "$ENV_FILE"
    echo "✅ .env fil opprettet fra template"
else
    echo "ℹ️ Oppdaterer eksisterende .env fil"
fi

echo ""
echo "🔑 Nå må du redigere .env filen og fylle inn de ekte API-nøklene:"
echo "   nano $ENV_FILE"
echo ""
echo "📋 Du trenger disse verdiene:"
echo "   - SHOPIFY_API_KEY: Din Shopify API nøkkel"
echo "   - SHOPIFY_API_SECRET: Din Shopify API secret"
echo "   - SHOPIFY_ACCESS_TOKEN: Din Shopify access token"
echo ""

# Spør om å åpne editor
read -p "Vil du åpne .env filen i nano nå? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    nano "$ENV_FILE"
fi

echo ""
echo "🛡️ SIKKERHETSTIPS:"
echo "   ✅ .env filen er allerede i .gitignore"
echo "   ✅ API-nøkler lagres IKKE i konfigurasjonsfiler"
echo "   ✅ Bruk environment variables i produksjon"
echo "   ⚠️ Del ALDRI .env filen med andre"
echo "   ⚠️ Commit ALDRI .env til git"

# Test API tilkobling
echo ""
read -p "Vil du teste Shopify API tilkoblingen? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧪 Tester Shopify API..."
    cd "$SCRIPT_DIR"
    python3 -c "
import os
from dotenv import load_dotenv
import requests

load_dotenv('.env')

shop_url = os.getenv('SHOPIFY_SHOP_URL')
access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')

if not shop_url or not access_token:
    print('❌ Manglende konfigurasjon i .env fil')
    exit(1)

# Test API tilkobling
url = f'https://{shop_url}/admin/api/2023-10/shop.json'
headers = {'X-Shopify-Access-Token': access_token}

try:
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        shop_data = response.json().get('shop', {})
        print(f'✅ API tilkobling OK!')
        print(f'   Butikk: {shop_data.get(\"name\", \"ukjent\")}')
        print(f'   Domene: {shop_data.get(\"domain\", \"ukjent\")}')
    else:
        print(f'❌ API feil: HTTP {response.status_code}')
        print(f'   Respons: {response.text[:200]}')
except Exception as e:
    print(f'❌ Tilkoblingsfeil: {e}')
"
fi

echo ""
echo "🎉 Setup fullført!"
echo "📘 Neste steg:"
echo "   - Test Shopify sync: python3 scripts/shopify_sync.py"
echo "   - Se dokumentasjon: docs/shopify-integration.md"