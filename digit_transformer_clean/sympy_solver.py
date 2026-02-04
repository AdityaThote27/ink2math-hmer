# sympy_solver.py
import sympy as sp

def solve_expression(expr_str):
    expr = sp.sympify(expr_str)
    return expr.evalf()
