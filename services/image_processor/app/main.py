from fastapi import FastAPI
from app.routers import image_router

app = FastAPI(title="IMAGE PROCESSOR")

# Register routers
app.include_router(image_router.router)
