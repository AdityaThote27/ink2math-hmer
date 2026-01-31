import sympy as sp


def solve_expression(expr: str):
    try:
        return sp.sympify(expr)
    except Exception:
        return None
