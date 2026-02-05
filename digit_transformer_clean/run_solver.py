import torch

from model import DigitTransformer
from dataset import get_test_sample
from sympy_solver import solve_expression
from multi_digit_infer import predict_multiple_digits, digits_to_number


# ===============================
# Device setup
# ===============================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ===============================
# Load trained model
# ===============================
def load_model(checkpoint_path):
    model = DigitTransformer()
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.to(device)
    model.eval()
    return model


# ===============================
# Day 9: Single-digit solver
# ===============================
def run_single_digit_solver(model):
    img, true_label = get_test_sample()
    img = img.to(device).unsqueeze(0)

    with torch.no_grad():
        logits = model(img)
        pred = logits.argmax(dim=1).item()

    print(f"True label: {true_label}")
    print(f"Predicted digit: {pred}")

    expression = f"{pred} + 3"
    result = solve_expression(expression)

    print("Expression:", expression)
    print("Result:", result)


# ===============================
# Day 10 Phase 1 & 2:
# Multi-digit + symbolic evaluation
# ===============================
def run_multi_digit_solver(model, digit_images, operator="+", operand=3):
    digits = predict_multiple_digits(model, digit_images, device)
    number = digits_to_number(digits)

    expression = f"{number} {operator} {operand}"
    result = solve_expression(expression)

    print("Predicted digits:", digits)
    print("Constructed number:", number)
    print("Expression:", expression)
    print("Result:", result)

    return result


# ===============================
# Day 10 Phase 3:
# Two-operand multi-digit solver
# ===============================
def run_two_operand_solver(
    model,
    left_digit_images,
    right_digit_images,
    operator="+"
):
    left_digits = predict_multiple_digits(model, left_digit_images, device)
    right_digits = predict_multiple_digits(model, right_digit_images, device)

    left_number = digits_to_number(left_digits)
    right_number = digits_to_number(right_digits)

    expression = f"{left_number} {operator} {right_number}"
    result = solve_expression(expression)

    print("Left digits:", left_digits)
    print("Right digits:", right_digits)
    print("Expression:", expression)
    print("Result:", result)

    return result


# ===============================
# Main entry point
# ===============================
if __name__ == "__main__":

    CHECKPOINT_PATH = "digit_transformer_clean/digit_transformer.pth"

    model = load_model(CHECKPOINT_PATH)

    print("\n=== Day 9: Single-Digit Test ===")
    run_single_digit_solver(model)

    print("\n=== Day 10: Multi-Digit Test ===")

    # Simulated multi-digit input
    img1, _ = get_test_sample()
    img2, _ = get_test_sample()
    img3, _ = get_test_sample()

    digit_images = [img1, img2, img3]

    run_multi_digit_solver(model, digit_images)

    print("\n=== Day 10: Two-Operand Multi-Digit Test ===")

    # Simulated two operands
    left_imgs = [get_test_sample()[0] for _ in range(3)]   # e.g. 381
    right_imgs = [get_test_sample()[0] for _ in range(2)]  # e.g. 24

    run_two_operand_solver(
        model,
        left_digit_images=left_imgs,
        right_digit_images=right_imgs,
        operator="+"
    )
