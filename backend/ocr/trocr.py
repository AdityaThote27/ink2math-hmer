from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

# Load model once (important for performance)
PROCESSOR = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-base-handwritten"
)
MODEL = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-handwritten"
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL.to(DEVICE)


def run_ocr(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")

    pixel_values = PROCESSOR(
        images=image, return_tensors="pt"
    ).pixel_values.to(DEVICE)

    generated_ids = MODEL.generate(pixel_values)

    text = PROCESSOR.batch_decode(
        generated_ids, skip_special_tokens=True
    )[0]

    return text.strip()

