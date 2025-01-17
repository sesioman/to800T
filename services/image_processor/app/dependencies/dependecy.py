import os
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session
from app.services.storage_service import StorageService
from app.services.minio_storage_service import MinIOStorageService
from app.config import Config


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


def get_storage_service() -> StorageService:
    """
    Factory function to provide the appropriate StorageService implementation.
    This example uses environment variables to decide the storage type.
    """
    storage_type = Config.STORAGE_TYPE

    if storage_type == "none":
        return StorageService
    
    elif storage_type == "minio":
        return MinIOStorageService(
            endpoint=Config.MINIO_URL,
            access_key=Config.MINIO_ROOT_USER,
            secret_key=Config.MINIO_ROOT_PASSWORD,
            secure=Config.MINIO_SECURE
        )
    # You can add more storage backends here
    raise ValueError(f"Unsupported storage type: {storage_type}")