# app/routers/image_router.py

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, File, Form, UploadFile, Depends
from app.services.image_service import ImageService
from app.schemas.image_schema import ImageProcessedResponse, ImageCreatedResponse

router = APIRouter(prefix="/image-processor", tags=["Images"])


@router.post("/")
async def process_image(
    background_tasks: BackgroundTasks,
    width: Annotated[int, Form()],
    height: Annotated[int, Form()],
    file: UploadFile = File(...),
    service: ImageService = Depends(ImageService)) -> ImageCreatedResponse:
    """
    Sube una imagen para procesarla
    """
    return await service.process_image(file, width, height, background_tasks)

@router.get("/{image_id}")
async def get_image(image_id: UUID, service: ImageService = Depends(ImageService)) -> ImageProcessedResponse:
    """
    Obtiene información de una imagen procesada.
    """
    return await service.get_image_by_id(image_id)
