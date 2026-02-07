import cv2
import numpy as np


def segment_symbols(
    binary_image: np.ndarray,
    min_area: int = 100,
    debug: bool = False
):
    """
    Segments individual symbols from a preprocessed binary image.

    Args:
        binary_image: output of preprocess_image (white symbols on black)
        min_area: minimum contour area to keep
        debug: visualize bounding boxes if True

    Returns:
        List of cropped symbol images (numpy arrays), sorted left-to-right
    """

    # Find contours
    contours, _ = cv2.findContours(
        binary_image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    symbol_boxes = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h

        if area >= min_area:
            symbol_boxes.append((x, y, w, h))

    # Sort left-to-right
    symbol_boxes = sorted(symbol_boxes, key=lambda b: b[0])

    symbols = []

    for (x, y, w, h) in symbol_boxes:
        crop = binary_image[y:y+h, x:x+w]
        symbols.append(crop)

        if debug:
            cv2.rectangle(
                binary_image,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                1
            )

    if debug:
        cv2.imshow("Segmented Symbols", binary_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return symbols
