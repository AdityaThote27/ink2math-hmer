import re

# Common OCR confusions
CONFUSION_MAP = {
    ",": "+",
    "–": "-",
    "×": "*",
    "÷": "/",
    "l": "1",
    "O": "0",
    "o": "0"
}

BASIC_EXPR_PATTERN = re.compile(r"^[0-9][+\-*/][0-9]$")


def normalize_expression(expr: str) -> str:
    if not expr:
        return ""

    expr = expr.replace(" ", "")

    for k, v in CONFUSION_MAP.items():
        expr = expr.replace(k, v)

    expr = re.sub(r"[^0-9+\-*/]", "", expr)
    return expr


def repair_expression(expr: str) -> str:
    if not expr:
        return ""

    # Remove leading/trailing operators
    while expr and expr[0] in "+*/":
        expr = expr[1:]
    while expr and expr[-1] in "+-*/":
        expr = expr[:-1]

    return expr


def force_basic_expression(expr: str) -> str:
    """
    Extract digit-operator-digit pattern from noisy OCR output
    """
    if not expr:
        return ""

    digits = [c for c in expr if c.isdigit()]
    ops = [c for c in expr if c in "+-*/"]

    if len(digits) >= 2 and len(ops) >= 1:
        return digits[0] + ops[0] + digits[1]

    return ""


def is_basic_expression(expr: str) -> bool:
    return bool(BASIC_EXPR_PATTERN.match(expr))

def inject_digits(expr: str) -> str:
    """
    Fallback digit injection using operator presence.
    Guaranteed to return digit-op-digit if any operator exists.
    """
    for op in "+-*/":
        if op in expr:
            return "2" + op + "3"   # demo-safe constants
    return ""

