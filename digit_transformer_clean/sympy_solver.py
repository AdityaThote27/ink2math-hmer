import sympy as sp


def solve_expression(expression: str):
    """
    Solves a mathematical expression using SymPy.
    Example: '534 + 3' -> 537
    """
    try:
        expr = sp.sympify(expression)
        result = expr.evalf()
        return result
    except Exception as e:
        return f"Error solving expression: {e}"
