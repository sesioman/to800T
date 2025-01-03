# app/services/image_service.py
from app.repositories.image_repository import ImageRepository
from app.schemas.image_schema import ImageResponse, ProcessImageRequest
from fastapi import Depends, UploadFile
from app.utils.image_utils import save_image_to_disk

class ImageService:
    def __init__(self, repository: ImageRepository = Depends(ImageRepository)):
        self.repository = repository

    async def process_image(self, file: UploadFile, width: int, height: int) -> ImageResponse:
        # Guardar la imagen en disco (simulación)
        
        
        process_image_req: ProcessImageRequest = {
            "width": width,
            "height": height,
            "size": file.size,
            "format": file.content_type,
            "is_processed": False
        }
        image = await self.repository.create(process_image_req)
        file_path = save_image_to_disk(file, image.id)
        return image

    async def get_image_by_id(self, image_id: int) -> ImageResponse:
        return self.repository.get_by_id(image_id)
