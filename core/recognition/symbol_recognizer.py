import torch
import cv2
import numpy as np

from digit_transformer_clean.model import DigitTransformer
from core.recognition.operator_detector import detect_operator


class SymbolRecognizer:
    """
    Hybrid symbol recognizer:
    - Detects operators using rule-based heuristics
    - Falls back to CNN for digit recognition
    """

    def __init__(self, checkpoint_path: str, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Load trained digit model
        self.model = DigitTransformer().to(self.device)
        self.model.load_state_dict(
            torch.load(checkpoint_path, map_location=self.device)
        )
        self.model.eval()

    def recognize_digits(self, symbol_images):
        """
        Digit-only recognition (legacy support).
        """
        predictions = []

        with torch.no_grad():
            for img in symbol_images:
                img = self._prepare_digit(img)
                logits = self.model(img)
                pred = logits.argmax(dim=1).item()
                predictions.append(pred)

        return predictions

    def recognize_symbols(self, symbol_images):
        """
        Hybrid recognition: operators + digits.

        Returns:
            List[str] e.g. ['5', '3', '+', '4', '*', '7']
        """
        symbols = []

        with torch.no_grad():
            for img in symbol_images:
                # 1️⃣ Try operator detection first
                operator = detect_operator(img)
                if operator is not None:
                    symbols.append(operator)
                    continue

                # 2️⃣ Fallback to digit CNN
                img_tensor = self._prepare_digit(img)
                logits = self.model(img_tensor)
                pred = logits.argmax(dim=1).item()
                symbols.append(str(pred))

        return symbols

    def _prepare_digit(self, img):
        """
        Prepares a symbol image for digit CNN input.
        """
        # Ensure grayscale
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Resize
        img = cv2.resize(img, (64, 64))

        # Normalize
        img = img.astype(np.float32) / 255.0

        # Shape: (1, 1, 64, 64)
        tensor = torch.from_numpy(img).unsqueeze(0).unsqueeze(0)
        return tensor.to(self.device)
