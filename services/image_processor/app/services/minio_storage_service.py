from datetime import timedelta
import io
import os
from minio import Minio
from minio.error import S3Error
from app.services.storage_service import StorageService
from app.config import Config

class MinIOStorageService(StorageService):
    def __init__(self, endpoint: str, access_key: str, secret_key: str, secure: bool = False):
        """
        Initializes the MinIO client.
        :param endpoint: URL of the MinIO server (e.g., 'localhost:9000').
        :param access_key: Access key for authentication.
        :param secret_key: Secret key for authentication.
        :param secure: Defines whether to use HTTPS (True) or HTTP (False).
        """
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    def upload_file(self, file_data: bytes, file_name: str, bucket_name: str) -> str:
        try:
            # Check if the bucket exists, create it if it doesn't
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)

            # Upload the file
            self.client.put_object(
                bucket_name,
                file_name,
                data=io.BytesIO(file_data),
                length=len(file_data),
                content_type="image/png"
            )

            # Generate the file URL
            return f"http://{Config.MINIO_URL}/{bucket_name}/{file_name}"
        except S3Error as err:
            raise Exception(f"Error uploading file to MinIO: {err}")

    def get_file(self, file_name: str, bucket_name: str) -> bytes:
        try:
            response = self.client.get_object(bucket_name, file_name)
            return response.read()
        except S3Error as err:
            raise Exception(f"Error retrieving file from MinIO: {err}")

    def delete_file(self, file_name: str, bucket_name: str) -> None:
        try:
            self.client.remove_object(bucket_name, file_name)
        except S3Error as err:
            raise Exception(f"Error deleting file from MinIO: {err}")
        
    async def generate_presigned_url(self, bucket_name: str, file_name: str, expiry: int = 3600) -> str:
        try:
            url = self.client.presigned_get_object(
                bucket_name=bucket_name,
                object_name=file_name,
                expires=timedelta(seconds=expiry)
            )
            return url
        except Exception as e:
            raise Exception(f"Error generating presigned URL: {e}")
