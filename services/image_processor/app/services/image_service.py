# app/services/image_service.py
from uuid import UUID
from app.repositories.image_repository import ImageRepository
from app.schemas.image_schema import ImageCreatedResponse, ProcessImageRequest
from fastapi import Depends, UploadFile, BackgroundTasks
from app.utils.image_utils import save_image_to_disk
from app.cinestill_emulation.image_processor import ImageProcessor
from app.services.storage_service import StorageService
from app.dependencies.dependecy import get_storage_service
from app.utils.image_utils import sanitize_filename
from app.models.images import Image

bucket_name = "images"

class ImageService:
    def __init__(
            self,
            repository: ImageRepository = Depends(ImageRepository),
            image_processor: ImageProcessor = Depends(ImageProcessor),
            storage_service: StorageService = Depends(get_storage_service)
            ):
        self.repository = repository
        self.image_processor = image_processor
        self.storage_service = storage_service

    async def process_image(self, file: UploadFile, width: int, height: int, background_tasks: BackgroundTasks) -> ImageCreatedResponse:
        
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
        background_tasks.add_task(self.__process_and_update, unprocessed_file_path, processed_file_path, image.id)
        return image

    async def __process_and_update(self,file_path, out_path, image_id):
        print('Processing image')
        await self.image_processor.process_image(file_path, out_path)
        file_name: str
        image_bytes: bytes
        with open(out_path, 'rb') as image_file:
            file_name = sanitize_filename(image_file.name)
            image_bytes = image_file.read()
            self.storage_service.upload_file(file_data=image_bytes, file_name=file_name, bucket_name=bucket_name)
        await self.repository.update(image_id, {
            "size": len(image_bytes),
            "format": "image/png",
            "is_processed": True,
        })
        print('Finished processing')


    async def get_image_by_id(self, image_id: UUID):
        image = await self.repository.get_by_id(image_id)
        if not image.is_processed:
            image.url = None
        else:
            image.url = await self.storage_service.generate_presigned_url(bucket_name, f"{image_id}.png")
        return image

