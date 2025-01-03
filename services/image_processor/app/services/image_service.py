# app/services/image_service.py
import asyncio
from app.repositories.image_repository import ImageRepository
from app.schemas.image_schema import ImageResponse, ProcessImageRequest
from fastapi import Depends, UploadFile, BackgroundTasks
from app.utils.image_utils import save_image_to_disk
from app.cinestill_emulation.image_processor import ImageProcessor


image_processor = ImageProcessor()

class ImageService:
    def __init__(self, repository: ImageRepository = Depends(ImageRepository)):
        self.repository = repository

    async def process_image(self, file: UploadFile, width: int, height: int, background_tasks: BackgroundTasks) -> ImageResponse:
        
        process_image_req: ProcessImageRequest = {
            "width": width,
            "height": height,
            "size": file.size,
            "format": file.content_type,
            "is_processed": False
        }
        image = await self.repository.create(process_image_req)
        unprocessed_file_path = save_image_to_disk(file, image.id)
        processed_file_path = './processed/{}.png'.format(image.id)
        print("hola")
        print(unprocessed_file_path)
        background_tasks.add_task(self.__process_and_update, unprocessed_file_path, processed_file_path, image.id)
        return image

    async def __process_and_update(self,file_path, out_path, image_id):
        await image_processor.process_image(file_path, out_path)
        await self.repository.update(image_id, {
            "is_processed": True
        })


    async def get_image_by_id(self, image_id: int) -> ImageResponse:
        return self.repository.get_by_id(image_id)
