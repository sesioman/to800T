from typing import Any

from fastapi import Depends
import sqlalchemy
from app.dependencies.dependecy import get_session
from app.models.images import Image
from sqlalchemy.ext.asyncio import AsyncSession

class ImageRepository:
    def __init__(self, async_session: AsyncSession = Depends(get_session)):
        self.async_session = async_session

    async def create(self, image_data: dict) -> Image:
        new_image = Image(**image_data)
        self.async_session.add(new_image)
        await self.async_session.commit()
        await self.async_session.refresh(new_image)
        return new_image

    async def get_by_id(self, image_id: int) -> Image:
        stmt = sqlalchemy.select(Image).where(Image.id == image_id)
        query = await self.async_session.execute(stmt)
        image = query.scalar()
        if not image:
            raise ValueError(f"Image with id {image_id} not found.")
        return image
