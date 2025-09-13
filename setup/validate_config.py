#!/usr/bin/env python3
"""
Validate environment configuration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import *

def validate_config():
    """Validate all configuration settings"""
    print("🔍 Validating configuration...")
    
    errors = []
    warnings = []
    
    # Check environment variables
    print("\n📋 Environment Variables:")
    
    required_vars = {
        'SHOPIFY_SHOP': SHOPIFY_SHOP,
        'SHOPIFY_ACCESS_TOKEN': SHOPIFY_ACCESS_TOKEN,
        'MINIO_ACCESS_KEY': MINIO_ACCESS_KEY,
        'MINIO_SECRET_KEY': MINIO_SECRET_KEY,
    }
    
    for var_name, var_value in required_vars.items():
        if var_value:
            # Mask sensitive values
            if 'TOKEN' in var_name or 'KEY' in var_name:
                display_value = f"{var_value[:8]}...{var_value[-4:]}" if len(var_value) > 12 else "***"
            else:
                display_value = var_value
            print(f"   ✅ {var_name}: {display_value}")
        else:
            print(f"   ❌ {var_name}: Missing")
            errors.append(f"Missing required environment variable: {var_name}")
    
    optional_vars = {
        'MINIO_ENDPOINT': MINIO_ENDPOINT,
        'MINIO_BUCKET': MINIO_BUCKET,
        'MINIO_SECURE': MINIO_SECURE,
        'DATA_ROOT': DATA_ROOT,
    }
    
    for var_name, var_value in optional_vars.items():
        print(f"   ℹ️ {var_name}: {var_value}")
    
    # Test cloud storage connection
    print("\n☁️ Testing cloud storage connection...")
    try:
        result = subprocess.run(["rclone", "lsd", "gdrive:"], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Google Drive connection successful")
        else:
            errors.append("Google Drive connection failed")
            
        result = subprocess.run(["rclone", "lsd", "jottacloud:"], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Jottacloud connection successful")
        else:
            errors.append("Jottacloud connection failed")
    except Exception as e:
        errors.append(f"Cloud storage validation failed: {e}")
        print(f"   ❌ Connection failed: {e}")
    
    # Validate Shopify settings
    print("\n🛍️ Validating Shopify settings...")
    
    if SHOPIFY_SHOP:
        if not SHOPIFY_SHOP.endswith('.myshopify.com'):
            warnings.append("SHOPIFY_SHOP should end with '.myshopify.com'")
            print(f"   ⚠️ Shop domain format may be incorrect")
        else:
            print(f"   ✅ Shop domain format looks correct")
    
    if SHOPIFY_ACCESS_TOKEN:
        if not SHOPIFY_ACCESS_TOKEN.startswith('shpat_'):
            warnings.append("SHOPIFY_ACCESS_TOKEN should start with 'shpat_'")
            print(f"   ⚠️ Access token format may be incorrect")
        else:
            print(f"   ✅ Access token format looks correct")
    
    # Check file system permissions
    print("\n📁 Checking file system...")
    
    import pathlib
    data_path = pathlib.Path(DATA_ROOT)
    
    try:
        data_path.mkdir(exist_ok=True)
        test_file = data_path / '.test_write'
        test_file.write_text('test')
        test_file.unlink()
        print(f"   ✅ Write access to {data_path.resolve()}")
    except Exception as e:
        errors.append(f"Cannot write to data directory {data_path}: {e}")
        print(f"   ❌ Write access failed: {e}")
    
    # Summary
    print("\n" + "="*50)
    print("📊 Configuration Summary:")
    
    if errors:
        print(f"❌ {len(errors)} critical errors found:")
        for error in errors:
            print(f"   • {error}")
    
    if warnings:
        print(f"⚠️ {len(warnings)} warnings:")
        for warning in warnings:
            print(f"   • {warning}")
    
    if not errors and not warnings:
        print("✅ All configuration checks passed!")
        print("\nYou're ready to run:")
        print("   python main.py bootstrap")
    elif not errors:
        print("✅ Configuration is functional with minor warnings")
        print("\nYou can proceed with:")
        print("   python main.py bootstrap")
    else:
        print("❌ Critical errors must be fixed before proceeding")
        print("\nPlease:")
        print("1. Fix the errors listed above")
        print("2. Update your .env file")
        print("3. Run this validation again")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = validate_config()
    sys.exit(0 if success else 1)