from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

# Load model once
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

def recognize_math_expression(image_path: str) -> str:
    try:
        image = Image.open(image_path).convert("RGB")

        pixel_values = processor(images=image, return_tensors="pt").pixel_values

        with torch.no_grad():
            generated_ids = model.generate(pixel_values)

        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return generated_text.strip()

    except Exception as e:
        print("TrOCR Error:", e)
        return None
