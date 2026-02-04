from sympy_solver import solve_expression

digit = 7
expr = f"{digit} + 3"

result = solve_expression(expr)
print("Expression:", expr)
print("Result:", result)
