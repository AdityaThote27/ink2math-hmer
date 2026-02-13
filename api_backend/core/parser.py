from sympy import symbols
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application
)

# Enable implicit multiplication (e.g., 3x → 3*x)
transformations = (
    standard_transformations + (implicit_multiplication_application,)
)

def parse_expression(expression: str):
    try:
        # Replace caret with Python power operator
        expression = expression.replace("^", "**")

        # Handle equations with '='
        if "=" in expression:
            left, right = expression.split("=")

            left_expr = parse_expr(left.strip(), transformations=transformations)
            right_expr = parse_expr(right.strip(), transformations=transformations)

            # Convert equation to standard form: left - right = 0
            return left_expr - right_expr

        # If no '=', just parse directly
        return parse_expr(expression.strip(), transformations=transformations)

    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")
