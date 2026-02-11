from sympy import sympify

def parse_expression(expression: str):
    try:
        # Replace caret with Python power operator
        expression = expression.replace("^", "**")

        # Handle equations with =
        if "=" in expression:
            left, right = expression.split("=")
            left_expr = sympify(left.strip())
            right_expr = sympify(right.strip())

            # Convert equation to standard form: left - right = 0
            return left_expr - right_expr

        # If no '=', just parse directly
        return sympify(expression)

    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")
