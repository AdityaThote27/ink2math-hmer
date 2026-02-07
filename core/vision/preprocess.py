import cv2
import numpy as np


def preprocess_image(
    image_path: str,
    debug: bool = False
) -> np.ndarray:
    """
    Preprocess a handwritten math image for segmentation.

    Steps:
    1. Load image
    2. Convert to grayscale
    3. Noise reduction
    4. Adaptive thresholding
    5. Morphological cleanup

    Returns:
        Binary image (numpy array) suitable for contour detection
    """

    # -------------------------------
    # 1. Load image
    # -------------------------------
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")

    # -------------------------------
    # 2. Convert to grayscale
    # -------------------------------
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # -------------------------------
    # 3. Noise reduction
    # -------------------------------
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # -------------------------------
    # 4. Adaptive thresholding
    # -------------------------------
    binary = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    # -------------------------------
    # 5. Morphological cleanup
    # -------------------------------
    kernel = np.ones((3, 3), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # -------------------------------
    # Debug visualization
    # -------------------------------
    if debug:
        cv2.imshow("Original", image)
        cv2.imshow("Grayscale", gray)
        cv2.imshow("Binary", cleaned)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return cleaned
