from backend.ocr.trocr import run_ocr

# CHANGE THIS to an actual processed image filename
IMAGE_PATH = "C:\\Users\\adity\\OneDrive\\Documents\\Projects\\ink2math-hmer\\backend\\outputs\\mathsequation.png"

result = run_ocr(IMAGE_PATH)
print("OCR OUTPUT:", result)
