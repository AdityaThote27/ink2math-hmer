from sympy import symbols, solve

def solve_expression(expr):
    x = symbols('x')
    solution = solve(expr, x)

    # If single solution, return just value
    if len(solution) == 1:
        return solution[0]

    return solution
