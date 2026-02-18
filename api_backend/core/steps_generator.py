from sympy import Poly

def generate_steps(parsed_expr, solution):
    steps = []
    step_number = 1

    # 🔍 Detect if expression contains variables
    has_variable = bool(parsed_expr.free_symbols)

    # ==============================
    # CASE 1 — PURE ARITHMETIC
    # ==============================
    if not has_variable:
        steps.append({
            "step": step_number,
            "title": "Evaluate Expression",
            "description": f"Compute the value of {str(parsed_expr)}."
        })
        step_number += 1

        steps.append({
            "step": step_number,
            "title": "Final Answer",
            "description": f"{str(solution)}"
        })

        return steps

    # ==============================
    # CASE 2 — EQUATION
    # ==============================

    variable = list(parsed_expr.free_symbols)[0]

    # STEP 1 — Standard Form
    steps.append({
        "step": step_number,
        "title": "Standard Form",
        "description": f"{str(parsed_expr)} = 0"
    })
    step_number += 1

    # Detect polynomial degree safely
    try:
        poly = Poly(parsed_expr, variable)
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
            "title": "Solve for Variable",
            "description": f"Isolate {variable}."
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
            "description": "Simplify the equation if possible."
        })
        step_number += 1

    # FINAL STEP — Format Solution
    if isinstance(solution, list):
        if len(solution) == 1:
            sol_text = f"{variable} = {str(solution[0])}"
        else:
            sol_text = ", ".join([f"{variable} = {str(s)}" for s in solution])
    else:
        sol_text = f"{variable} = {str(solution)}"

    steps.append({
        "step": step_number,
        "title": "Final Answer",
        "description": sol_text
    })

    return steps
