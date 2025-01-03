# app/schemas/image_schema.py
from uuid import UUID
from fastapi import UploadFile
from pydantic import BaseModel

class ImageResponse(BaseModel):
    id: UUID
    file_path: str | None
    width: int
    height: int
    size: int
    format: str | None
    is_processed: bool

class ProcessImageRequest(BaseModel):
    width: int
    height: int
    size: int
    format: str | None