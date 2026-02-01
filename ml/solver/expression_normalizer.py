import re

OPERATORS = {"+", "-", "*", "/", "^"}


def normalize_expression(expr: str) -> str | None:
    """
    Normalize noisy OCR output into a valid math expression.
    Returns cleaned expression or None if invalid.
    """

    if not expr or not any(ch.isdigit() for ch in expr):
        return None

    # Remove spaces
    expr = expr.replace(" ", "")

    # Fix common OCR spacing issues
    expr = expr.replace("+-", "-")
    expr = expr.replace("--", "+")

    # Remove trailing operators
    while len(expr) > 0 and expr[-1] in OPERATORS:
        expr = expr[:-1]

    # Remove leading operators except minus
    while len(expr) > 0 and expr[0] in OPERATORS and expr[0] != "-":
        expr = expr[1:]

    # Validate final expression
    if not expr or not any(ch.isdigit() for ch in expr):
        return None

    # Final safety regex
    if not re.fullmatch(r"[0-9+\-*/^()]+", expr):
        return None

    return expr
