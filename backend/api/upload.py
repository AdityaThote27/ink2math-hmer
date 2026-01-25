import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
from backend.preprocessing.image import preprocess_image

router = APIRouter()

UPLOAD_DIR = "backend/outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-image", tags=["Input"])
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        processed_path = preprocess_image(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Image uploaded and processed",
        "original_image": file_path,
        "processed_image": processed_path
    }
