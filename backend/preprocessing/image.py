import cv2
import os


def preprocess_image(input_path: str) -> str:
    image = cv2.imread(input_path)

    if image is None:
        raise ValueError("Failed to read image")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (512, 512))

    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    output_dir = "backend/outputs/processed"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir, os.path.basename(input_path)
    )

    cv2.imwrite(output_path, thresh)

    return output_path
