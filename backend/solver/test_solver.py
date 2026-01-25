from backend.solver.sympy_solver import solve_equation

# Try with OCR-like text
samples = [
    "x^2 + 5x + 6 = 0",
    "x2+5x+6=0",
    "x² + 5 x + 6 = 0"
]

for text in samples:
    result = solve_equation(text)
    print("\nINPUT:", text)
    print("OUTPUT:", result)
