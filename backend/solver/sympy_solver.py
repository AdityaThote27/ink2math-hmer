import sympy as sp
import re


def clean_ocr_text(text: str) -> str:
    """
    Cleans common OCR mistakes for basic algebraic equations.
    Designed for robustness, not perfection.
    """
    text = text.lower().strip()

    # Normalize unicode superscripts
    text = text.replace("²", "**2")
    text = text.replace("³", "**3")

    # Remove spaces
    text = text.replace(" ", "")

    # Normalize operators
    text = text.replace("×", "*")
    text = text.replace("^", "**")

    # Fix common OCR dot mistakes
    # Example: x.6.0 -> x+6=0
    text = text.replace(".=", "=")
    text = text.replace(".0", "=0")

    # Replace stray dots between terms with +
    text = re.sub(r"([a-zA-Z0-9])\.([a-zA-Z0-9])", r"\1+\2", text)

    # Convert x2 -> x**2
    text = re.sub(r"x(\d+)", r"x**\1", text)

    # Fix implicit multiplication: 2x -> 2*x
    text = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", text)

    return text


def solve_equation(ocr_text: str):
    """
    Solves a single-variable algebraic equation using SymPy.
    Returns JSON-safe output.
    """
    x = sp.symbols("x")

    cleaned = clean_ocr_text(ocr_text)

    try:
        if "=" in cleaned:
            left, right = cleaned.split("=")
            expr = sp.sympify(left) - sp.sympify(right)
        else:
            expr = sp.sympify(cleaned)
    except Exception as e:
        return {
            "success": False,
            "error": f"Parsing failed: {str(e)}",
            "cleaned_text": cleaned
        }

    try:
        solutions = sp.solve(expr, x)
    except Exception as e:
        return {
            "success": False,
            "error": f"Solving failed: {str(e)}",
            "cleaned_text": cleaned
        }

    return {
        "success": True,
        "original_text": ocr_text,
        "cleaned_text": cleaned,
        "solutions": [str(sol) for sol in solutions]
    }
