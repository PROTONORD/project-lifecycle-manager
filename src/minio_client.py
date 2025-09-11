import io
from minio import Minio
from minio.error import S3Error
from typing import BinaryIO, Optional

def create_minio_client(endpoint: str, access_key: str, secret_key: str, secure: bool) -> Minio:
    """Create MinIO client instance"""
    return Minio(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )

def ensure_bucket_exists(client: Minio, bucket_name: str) -> None:
    """Ensure bucket exists, create if it doesn't"""
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Created bucket: {bucket_name}")
    except S3Error as e:
        print(f"Error ensuring bucket exists: {e}")
        raise

def upload_bytes_to_minio(
    client: Minio, 
    bucket: str, 
    object_name: str, 
    data: bytes, 
    content_type: str = "application/octet-stream"
) -> None:
    """Upload bytes data to MinIO"""
    try:
        data_stream = io.BytesIO(data)
        client.put_object(
            bucket_name=bucket,
            object_name=object_name,
            data=data_stream,
            length=len(data),
            content_type=content_type
        )
        print(f"Uploaded {object_name} to {bucket}")
    except S3Error as e:
        print(f"Error uploading {object_name}: {e}")
        raise

def upload_file_to_minio(
    client: Minio,
    bucket: str,
    object_name: str,
    file_path: str,
    content_type: Optional[str] = None
) -> None:
    """Upload file to MinIO"""
    try:
        client.fput_object(
            bucket_name=bucket,
            object_name=object_name,
            file_path=file_path,
            content_type=content_type
        )
        print(f"Uploaded {file_path} as {object_name} to {bucket}")
    except S3Error as e:
        print(f"Error uploading file {file_path}: {e}")
        raise

def get_object_url(client: Minio, bucket: str, object_name: str, expires_hours: int = 24) -> str:
    """Generate presigned URL for object"""
    try:
        from datetime import timedelta
        url = client.presigned_get_object(
            bucket_name=bucket,
            object_name=object_name,
            expires=timedelta(hours=expires_hours)
        )
        return url
    except S3Error as e:
        print(f"Error generating URL for {object_name}: {e}")
        raise