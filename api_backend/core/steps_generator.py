from sympy import symbols, Poly

def generate_steps(parsed_expr, solution):
    steps = []
    step_number = 1

    x = symbols('x')

    # STEP 1 — Standard Form
    steps.append({
        "step": step_number,
        "title": "Standard Form",
        "description": f"{str(parsed_expr)} = 0"
    })
    step_number += 1

    # Detect polynomial degree
    try:
        poly = Poly(parsed_expr, x)
        degree = poly.degree()
    except Exception:
        degree = None

    # STEP 2+ — Based on Equation Type
    if degree == 1:
        steps.append({
            "step": step_number,
            "title": "Identify Equation Type",
            "description": "Detected Linear Equation (degree 1)."
        })
        step_number += 1

        steps.append({
            "step": step_number,
            "title": "Isolate Variable",
            "description": "Rearrange equation to isolate x."
        })
        step_number += 1

    elif degree == 2:
        steps.append({
            "step": step_number,
            "title": "Identify Equation Type",
            "description": "Detected Quadratic Equation (degree 2)."
        })
        step_number += 1

        steps.append({
            "step": step_number,
            "title": "Apply Solving Method",
            "description": "Use factorization or quadratic formula."
        })
        step_number += 1

    else:
        steps.append({
            "step": step_number,
            "title": "Simplification",
            "description": "Simplify the expression if possible."
        })
        step_number += 1

    # FINAL STEP — Format Solution
    if isinstance(solution, list):
        if len(solution) == 1:
            sol_text = f"x = {str(solution[0])}"
        else:
            sol_text = "Solutions: " + ", ".join([f"x = {str(s)}" for s in solution])
    else:
        sol_text = f"x = {str(solution)}"

    steps.append({
        "step": step_number,
        "title": "Final Answer",
        "description": sol_text
    })

    return steps
