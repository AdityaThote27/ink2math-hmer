import cv2
import numpy as np


def detect_operator(symbol_img):
    """
    Conservative operator detection.
    Returns '+', '-', '*' or None.
    """

    h, w = symbol_img.shape
    area = h * w
    aspect_ratio = w / float(h)

    # -------------------------
    # Detect minus (-)
    # -------------------------
    if aspect_ratio > 3.0 and h < 0.3 * w:
        return "-"

    # -------------------------
    # Edge-based analysis
    # -------------------------
    edges = cv2.Canny(symbol_img, 50, 150)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 40)
    if lines is None:
        return None

    angles = [line[0][1] for line in lines]

    # -------------------------
    # Detect multiply (*)
    # -------------------------
    diagonal_lines = [
        a for a in angles
        if 0.6 < a < 1.0 or 2.1 < a < 2.5
    ]

    if len(diagonal_lines) >= 2:
        return "*"

    # -------------------------
    # Detect plus (+)
    # -------------------------
    vertical = any(abs(a - np.pi/2) < 0.15 for a in angles)
    horizontal = any(abs(a) < 0.15 or abs(a - np.pi) < 0.15 for a in angles)

    if vertical and horizontal:
        return "+"

    return None
