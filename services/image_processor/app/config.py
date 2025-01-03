import os
from dotenv import load_dotenv

# Detectar el entorno
environment = os.getenv("ENVIRONMENT", "local")

# Cargar .env solo en local
if environment == "local":
    load_dotenv()

# Configuración global
class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
