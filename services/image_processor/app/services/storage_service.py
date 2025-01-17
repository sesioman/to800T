from abc import ABC, abstractmethod

class StorageService(ABC):
    @abstractmethod
    def upload_file(self, file_data: bytes, file_name: str, bucket_name: str) -> str:
        """
        Uploads a file to the specified bucket.
        :param file_data: File content in bytes.
        :param file_name: Name of the file.
        :param bucket_name: Name of the bucket.
        :return: URL of the uploaded file.
        """
        pass

    @abstractmethod
    def get_file(self, file_name: str, bucket_name: str) -> bytes:
        """
        Downloads a file from the specified bucket.
        :param file_name: Name of the file to download.
        :param bucket_name: Name of the bucket.
        :return: File content in bytes.
        """
        pass

    @abstractmethod
    def delete_file(self, file_name: str, bucket_name: str) -> None:
        """
        Deletes a file from the specified bucket.
        :param file_name: Name of the file to delete.
        :param bucket_name: Name of the bucket.
        """
        pass
    
    async def generate_presigned_url(self, bucket_name: str, file_name: str, expiry: int = 3600) -> str:
        """
        Generates a presigned URL for accessing an object in MinIO.
        :param bucket_name: The bucket name.
        :param file_name: The file name.
        :param expiry: Expiration time in seconds (default: 3600 seconds, or 1 hour).
        :return: The presigned URL as a string.
        """
        pass