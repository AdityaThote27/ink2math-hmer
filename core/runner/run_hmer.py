from core.vision.preprocess import preprocess_image
from core.vision.segment import segment_symbols
from core.recognition.symbol_recognizer import SymbolRecognizer
from core.hmer.symbol_postprocess import clean_symbol_sequence
from digit_transformer_clean.sympy_solver import solve_expression


def run_hmer(image_path: str):
    print(f"\n[HMER] Processing image: {image_path}")

    # ---------------------------------
    # 1. Preprocess image
    # ---------------------------------
    binary_image = preprocess_image(image_path)

    # ---------------------------------
    # 2. Segment symbols
    # ---------------------------------
    symbol_images = segment_symbols(binary_image)

    print(f"[HMER] Segmented {len(symbol_images)} symbols")

    if not symbol_images:
        print("[HMER] No symbols detected. Exiting.")
        return

    # ---------------------------------
    # 3. Hybrid symbol recognition
    # ---------------------------------
    recognizer = SymbolRecognizer(
        checkpoint_path="digit_transformer_clean/digit_transformer.pth"
    )

    raw_symbols = recognizer.recognize_symbols(symbol_images)

    print("[HMER] Raw symbol predictions:", raw_symbols)

    # ---------------------------------
    # 4. Symbol post-processing (syntax cleanup)
    # ---------------------------------
    cleaned_symbols = clean_symbol_sequence(raw_symbols)

    print("[HMER] Cleaned symbols:", cleaned_symbols)

    if not cleaned_symbols:
        print("[HMER] Expression empty after cleanup. Exiting.")
        return

    # ---------------------------------
    # 5. Build expression string
    # ---------------------------------
    expression = "".join(cleaned_symbols)

    print("[HMER] Constructed expression:", expression)

    # ---------------------------------
    # 6. Evaluate expression
    # ---------------------------------
    result = solve_expression(expression)

    print("[HMER] Result:", result)


if __name__ == "__main__":
    IMAGE_PATH = "sample_math.png"
    run_hmer(IMAGE_PATH)
