#!/usr/bin/env python3
"""
Generate file catalog/index for GitHub that references files in MinIO
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from minio import Minio
from minio.error import S3Error
import argparse

class MinIOFileCatalogGenerator:
    def __init__(self, minio_client: Minio, base_url: str):
        self.minio = minio_client
        self.base_url = base_url
        
    def scan_product_files(self, product_handle: str) -> Dict[str, Any]:
        """Scan MinIO for files related to a product and generate catalog"""
        catalog = {
            "product_id": product_handle,
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "files": {
                "images": [],
                "cad": [],
                "documentation": []
            },
            "total_files": 0,
            "total_size_bytes": 0
        }
        
        # Scan different buckets for product files
        buckets_to_scan = {
            "products": "images",
            "cad-files": "cad", 
            "documentation": "documentation"
        }
        
        for bucket_name, file_type in buckets_to_scan.items():
            try:
                # List objects in bucket with product prefix
                prefix = f"{product_handle}/"
                objects = self.minio.list_objects(bucket_name, prefix=prefix, recursive=True)
                
                for obj in objects:
                    file_info = {
                        "filename": obj.object_name.split('/')[-1],
                        "minio_path": obj.object_name,
                        "size_bytes": obj.size,
                        "url": f"{self.base_url}/{bucket_name}/{obj.object_name}",
                        "uploaded": obj.last_modified.isoformat() + "Z" if obj.last_modified else None
                    }
                    
                    # Add description based on file type
                    if file_type == "cad":
                        ext = file_info["filename"].split('.')[-1].lower()
                        descriptions = {
                            "step": "3D CAD model - STEP format",
                            "stl": "3D print ready - STL format", 
                            "dwg": "AutoCAD drawing file",
                            "3mf": "3D Manufacturing Format"
                        }
                        file_info["description"] = descriptions.get(ext, f"{ext.upper()} file")
                        
                    catalog["files"][file_type].append(file_info)
                    catalog["total_files"] += 1
                    catalog["total_size_bytes"] += obj.size or 0
                    
            except S3Error as e:
                print(f"Warning: Could not access bucket {bucket_name}: {e}")
                
        return catalog
        
    def generate_files_json(self, product_handle: str, output_path: str):
        """Generate files.json catalog for a product"""
        catalog = self.scan_product_files(product_handle)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
            
        return catalog
        
    def generate_files_markdown(self, catalog: Dict[str, Any], output_path: str):
        """Generate FILES.md catalog for a product"""
        product_id = catalog["product_id"]
        
        md_content = f"""# {product_id.replace('-', ' ').title()} - Filkatalog

## 📁 Filer i MinIO Object Storage

"""
        
        # Generate tables for each file type
        file_types = {
            "images": {"title": "🖼️ Produktbilder", "bucket": "products"},
            "cad": {"title": "🔧 CAD-filer", "bucket": "cad-files"},
            "documentation": {"title": "📄 Dokumentasjon", "bucket": "documentation"}
        }
        
        for file_type, config in file_types.items():
            files = catalog["files"].get(file_type, [])
            if not files:
                continue
                
            md_content += f"### {config['title']}\n"
            md_content += f"Alle filer ligger i MinIO bucket: `{config['bucket']}`\n\n"
            
            if file_type == "cad":
                md_content += "| Fil | Format | Størrelse | Nedlastingslenke | Beskrivelse |\n"
                md_content += "|-----|--------|-----------|------------------|-------------|\n"
                for file_info in files:
                    filename = file_info["filename"]
                    size_str = self.format_file_size(file_info["size_bytes"])
                    url = file_info["url"]
                    desc = file_info.get("description", "")
                    ext = filename.split('.')[-1].upper()
                    md_content += f"| [{filename}]({url}) | {ext} | {size_str} | [Last ned]({url}) | {desc} |\n"
            else:
                md_content += "| Fil | Størrelse | Nedlastingslenke | Opplastet |\n"
                md_content += "|-----|-----------|------------------|----------|\n"
                for file_info in files:
                    filename = file_info["filename"]
                    size_str = self.format_file_size(file_info["size_bytes"])
                    url = file_info["url"]
                    uploaded = file_info.get("uploaded", "").split('T')[0] if file_info.get("uploaded") else "N/A"
                    md_content += f"| [{filename}]({url}) | {size_str} | [Last ned]({url}) | {uploaded} |\n"
                    
            md_content += "\n"
            
        # Add MinIO access information
        md_content += """## 🔗 Direkte MinIO tilgang

**MinIO Web Interface:** http://172.19.228.199:9001  
**Innlogging:** protonord-admin / [se .env fil for passord]

**Mappestier i MinIO:**"""

        for file_type, config in file_types.items():
            if catalog["files"].get(file_type):
                md_content += f"\n- `{config['bucket']}/{product_id}/`"
                
        total_files = catalog["total_files"]
        total_size = self.format_file_size(catalog["total_size_bytes"])
        md_content += f"\n\n---\n*Total: {total_files} filer, {total_size} lagret i MinIO*"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def main():
    parser = argparse.ArgumentParser(description="Generate file catalog for GitHub from MinIO content")
    parser.add_argument("product_handle", help="Product handle to generate catalog for")
    parser.add_argument("--output-dir", help="Output directory for catalog files")
    parser.add_argument("--minio-endpoint", default="127.0.0.1:9000", help="MinIO endpoint")
    parser.add_argument("--minio-access-key", default="protonord-admin", help="MinIO access key")
    parser.add_argument("--minio-secret-key", required=True, help="MinIO secret key")
    
    args = parser.parse_args()
    
    # Create MinIO client
    minio_client = Minio(
        args.minio_endpoint,
        access_key=args.minio_access_key,
        secret_key=args.minio_secret_key,
        secure=False
    )
    
    base_url = f"http://{args.minio_endpoint}"
    generator = MinIOFileCatalogGenerator(minio_client, base_url)
    
    # Generate catalog
    output_dir = args.output_dir or f"catalog/products/{args.product_handle}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate files.json
    files_json_path = os.path.join(output_dir, "files.json")
    catalog = generator.generate_files_json(args.product_handle, files_json_path)
    print(f"Generated: {files_json_path}")
    
    # Generate FILES.md  
    files_md_path = os.path.join(output_dir, "FILES.md")
    generator.generate_files_markdown(catalog, files_md_path)
    print(f"Generated: {files_md_path}")
    
    print(f"Found {catalog['total_files']} files totaling {generator.format_file_size(catalog['total_size_bytes'])}")


if __name__ == "__main__":
    main()