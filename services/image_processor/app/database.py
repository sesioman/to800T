from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import Config
from sqlalchemy.ext.declarative import declarative_base

# Crea el motor asíncrono de SQLAlchemy
engine = create_async_engine(Config.DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base(metadata=MetaData())

# Dependencia para obtener una sesión de la base de datos
async def get_db():
    async with async_session() as session:
        yield session
