import os
from dotenv import load_dotenv

# Detectar el entorno
environment = os.getenv("ENVIRONMENT", "local")

# Cargar .env solo en local
if environment == "local":
    load_dotenv()

def get_secret(secret_path: str, default_value: str = None) -> str:
    try:
        with open(secret_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        if default_value is not None:
            return default_value
        raise ValueError(f"Secret '{secret_path}' not found")

# Configuración global
class Config:
    
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASS = get_secret(os.getenv("DATABASE_PASS_FILE"), os.getenv("DATABASE_PASS"))
    DATABASE_NAME = os.getenv("DATABASE_NAME", "images_service")
    DATABASE_PORT = os.getenv("DATABASE_PORT", 5432)
    DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(DATABASE_USER, DATABASE_PASS, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    STORAGE_TYPE = os.getenv("STORAGE_TYPE", "none")
    MINIO_URL = os.getenv("MINIO_URL" ,"localhost:9000")
    MINIO_ROOT_USER = get_secret(os.getenv("MINIO_ROOT_USER_FILE"), os.getenv("MINIO_ROOT_USER", "minioadmin"))
    MINIO_ROOT_PASSWORD = get_secret(os.getenv("MINIO_ROOT_PASSWORD_FILE"), os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"))
    MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower == "true"


