import torch


def predict_multiple_digits(model, digit_images, device):
    """
    Predicts a sequence of digits from a list of digit images.

    Args:
        model: trained CNN-Transformer model
        digit_images: list of preprocessed digit tensors (C×H×W)
        device: torch device

    Returns:
        List of predicted digits (ints)
    """
    model.eval()
    predictions = []

    with torch.no_grad():
        for img in digit_images:
            img = img.to(device).unsqueeze(0)  # [1, C, H, W]
            logits = model(img)
            pred = logits.argmax(dim=1).item()
            predictions.append(pred)

    return predictions


def digits_to_number(digits):
    """
    Converts a digit sequence into a multi-digit number.
    Example: [1, 2, 3] -> 123
    """
    if not digits:
        raise ValueError("Digit sequence is empty")

    if not all(isinstance(d, int) and 0 <= d <= 9 for d in digits):
        raise ValueError("Invalid digit detected")

    return int("".join(map(str, digits)))
