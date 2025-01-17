# app/schemas/image_schema.py
from uuid import UUID
from pydantic import BaseModel

class ImageCreatedResponse(BaseModel):
    id: UUID
    width: int
    height: int
    size: int
    format: str | None
    is_processed: bool

class ImageProcessedResponse(BaseModel):
    id: UUID
    url: str | None
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