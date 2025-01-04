from fastapi import FastAPI
from app.routers import image_router
from app.config import Config

print(Config.DATABASE_URL)

app = FastAPI(title="IMAGE PROCESSOR")


# Register routers
app.include_router(image_router.router)
