# app/models/images.py
import uuid
from pydantic import BaseModel
from sqlalchemy import UUID, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from app.database import Base



class Image(Base):
    __tablename__ = "images_metadata"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    file_path = Column(String, nullable=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    format = Column(String, nullable=True)
    is_processed = Column(Boolean, default=False, nullable=False)
