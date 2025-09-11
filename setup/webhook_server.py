#!/usr/bin/env python3
"""
Simple webhook server for real-time Shopify updates
"""

import sys
import os
import json
import hmac
import hashlib
from flask import Flask, request, jsonify
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import validate
from src.bootstrap_catalog import create_product_folder, normalize_handle
from pathlib import Path

app = Flask(__name__)

# Configure webhook secret (set in environment)
WEBHOOK_SECRET = os.getenv('SHOPIFY_WEBHOOK_SECRET', '')

def verify_webhook(data, signature):
    """Verify Shopify webhook signature"""
    if not WEBHOOK_SECRET:
        app.logger.warning("No webhook secret configured - skipping verification")
        return True
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        data,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

@app.route('/webhook/shopify/product/create', methods=['POST'])
def handle_product_create():
    """Handle new product creation from Shopify"""
    try:
        # Verify webhook
        signature = request.headers.get('X-Shopify-Hmac-Sha256', '')
        if not verify_webhook(request.data, signature):
            app.logger.error("Invalid webhook signature")
            return jsonify({'error': 'Invalid signature'}), 401
        
        product_data = request.json
        app.logger.info(f"New product created: {product_data.get('title', 'Unknown')}")
        
        # Create local folder structure
        catalog_path = Path("catalog")
        catalog_path.mkdir(exist_ok=True)
        
        product_info = create_product_folder(catalog_path, product_data)
        
        # Log the creation
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event': 'product_created',
            'product_id': product_data.get('id'),
            'handle': product_info['handle'],
            'title': product_data.get('title'),
            'source': 'shopify_webhook'
        }
        
        # Append to webhook log
        with open('logs/webhook.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return jsonify({
            'status': 'success',
            'handle': product_info['handle'],
            'directory': product_info['directory']
        })
        
    except Exception as e:
        app.logger.error(f"Error handling product creation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/webhook/shopify/product/update', methods=['POST'])
def handle_product_update():
    """Handle product updates from Shopify"""
    try:
        # Verify webhook
        signature = request.headers.get('X-Shopify-Hmac-Sha256', '')
        if not verify_webhook(request.data, signature):
            app.logger.error("Invalid webhook signature")
            return jsonify({'error': 'Invalid signature'}), 401
        
        product_data = request.json
        handle = product_data.get('handle') or normalize_handle(product_data.get('title', ''))
        
        app.logger.info(f"Product updated: {product_data.get('title', 'Unknown')} ({handle})")
        
        # Check if local folder exists
        product_dir = Path("catalog") / handle
        if product_dir.exists():
            # Update local product.json if it exists
            product_json_path = product_dir / "product.json"
            if product_json_path.exists():
                # Update the local file with new data
                local_data = json.loads(product_json_path.read_text())
                
                # Update key fields that might have changed
                local_data.update({
                    'title': product_data.get('title'),
                    'status': product_data.get('status'),
                    'updated_at': product_data.get('updated_at'),
                    'body_html': product_data.get('body_html'),
                    'tags': product_data.get('tags'),
                })
                
                product_json_path.write_text(json.dumps(local_data, indent=2))
                app.logger.info(f"Updated local product.json for {handle}")
        
        # Log the update
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event': 'product_updated',
            'product_id': product_data.get('id'),
            'handle': handle,
            'title': product_data.get('title'),
            'source': 'shopify_webhook'
        }
        
        with open('logs/webhook.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return jsonify({'status': 'success', 'handle': handle})
        
    except Exception as e:
        app.logger.error(f"Error handling product update: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'shopify-webhook-receiver'
    })

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint with basic stats"""
    try:
        # Count products in catalog
        catalog_path = Path("catalog")
        product_count = 0
        if catalog_path.exists():
            product_count = len([d for d in catalog_path.iterdir() 
                               if d.is_dir() and (d / "product.json").exists()])
        
        # Get recent webhook activity
        webhook_log_path = Path("logs/webhook.log")
        recent_events = []
        if webhook_log_path.exists():
            with open(webhook_log_path, 'r') as f:
                lines = f.readlines()
                # Get last 10 events
                for line in lines[-10:]:
                    try:
                        recent_events.append(json.loads(line.strip()))
                    except:
                        continue
        
        return jsonify({
            'status': 'running',
            'timestamp': datetime.utcnow().isoformat(),
            'product_count': product_count,
            'recent_webhook_events': len(recent_events),
            'last_events': recent_events[-5:]  # Last 5 events
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Shopify Webhook Server')
    parser.add_argument('--port', type=int, default=8080, help='Port to run on')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/webhook.log'),
            logging.StreamHandler()
        ]
    )
    
    print(f"🚀 Starting Shopify webhook server on {args.host}:{args.port}")
    print(f"📡 Webhook endpoints:")
    print(f"   POST /webhook/shopify/product/create")
    print(f"   POST /webhook/shopify/product/update")
    print(f"   GET  /health")
    print(f"   GET  /status")
    
    app.run(host=args.host, port=args.port, debug=args.debug)