from sympy import solve

def solve_expression(parsed_expr):
    """
    Accepts already parsed sympy expression.
    Decides whether to simplify or solve.
    """

    # 🔍 If expression has variables → solve
    if parsed_expr.free_symbols:
        var = list(parsed_expr.free_symbols)[0]
        solution = solve(parsed_expr, var)

        if len(solution) == 1:
            return solution[0]

        return solution

    # 🧮 If no variables → just simplify
    return parsed_expr
