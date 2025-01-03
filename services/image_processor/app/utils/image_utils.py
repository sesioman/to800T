import shutil
from uuid import UUID
from fastapi import UploadFile
from pathlib import Path

def save_image_to_disk(file: UploadFile, image_id: UUID) -> str:
    """
    Saves an uploaded image to the specified directory.

    Args:
        file (UploadFile): The uploaded file object.

    Returns:
        str: The path to the saved image file.
    """

    output_dir = Path("./uploads/")
    output_dir.mkdir(exist_ok=True)  # Create the directory if it doesn't exist

    # Generate a unique filename
    extension = file.filename.split('.')[-1]
    file_path = output_dir / f"{image_id}.{extension}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)