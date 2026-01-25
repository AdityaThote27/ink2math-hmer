import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4

from backend.preprocessing.image import preprocess_image
from backend.ocr.trocr import run_ocr
from backend.solver.sympy_solver import solve_equation

router = APIRouter()

UPLOAD_DIR = "backend/outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/solve-image", tags=["Solve"])
async def solve_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    # Save uploaded image
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid4()}.{file_ext}"
    original_path = os.path.join(UPLOAD_DIR, file_name)

    with open(original_path, "wb") as f:
        f.write(await file.read())

    # Preprocess image
    try:
        processed_path = preprocess_image(original_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing failed: {str(e)}")

    # OCR
    try:
        ocr_text = run_ocr(processed_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

    # Solve equation
    result = solve_equation(ocr_text)

    return {
        "ocr_text": ocr_text,
        "result": result
    }
