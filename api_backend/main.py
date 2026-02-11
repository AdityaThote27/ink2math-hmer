from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from models.schemas import EquationRequest
from core.parser import parse_expression
from core.solver import solve_expression
from core.steps_generator import generate_steps
from core.utils import clean_input
from exports.pdf_export import generate_pdf
from exports.docx_export import generate_docx
from exports.braille_export import to_braille
from sympy import Poly, symbols, latex
import os

app = FastAPI()

# -------------------- CORS (Allow Frontend) --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

# -------------------- HOME --------------------
@app.get("/")
def home():
    return {"message": "Ink2Math Backend Running"}

# -------------------- SOLVE --------------------
@app.post("/solve")
def solve_equation(req: EquationRequest):
    try:
        # Step 1: Clean input
        cleaned = clean_input(req.expression)

        # Step 2: Parse expression
        parsed_expr = parse_expression(cleaned)

        # Step 3: Solve expression
        solution = solve_expression(parsed_expr)

        # Step 4: Clean solution formatting
        if isinstance(solution, list):
            if len(solution) == 1:
                clean_solution = str(solution[0])
            else:
                clean_solution = ", ".join([str(s) for s in solution])
        else:
            clean_solution = str(solution)

        # Step 5: Detect equation type
        x = symbols('x')
        try:
            poly = Poly(parsed_expr, x)
            degree = poly.degree()
        except:
            degree = None

        if degree == 1:
            equation_type = "Linear Equation"
        elif degree == 2:
            equation_type = "Quadratic Equation"
        else:
            equation_type = "General Expression"

        # Step 6: Generate dynamic steps
        steps = generate_steps(parsed_expr, solution)

        # Step 7: Generate LaTeX
        latex_expr = latex(parsed_expr)

        return {
            "input": str(req.expression),
            "type": equation_type,
            "solution": clean_solution,
            "latex": latex_expr,
            "steps": [
                {
                    "step": step["step"],
                    "title": step["title"],
                    "description": str(step["description"])
                }
                for step in steps
            ]
        }

    except Exception as e:
        return {"error": str(e)}

# -------------------- EXPORT PDF --------------------
@app.post("/export/pdf")
def export_pdf(req: EquationRequest):
    cleaned = clean_input(req.expression)
    parsed_expr = parse_expression(cleaned)
    solution = solve_expression(parsed_expr)
    steps = generate_steps(parsed_expr, solution)

    filename = "solution.pdf"
    filepath = os.path.join("static", filename)

    generate_pdf(filepath, req.expression, str(solution), steps)

    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=filename
    )

# -------------------- EXPORT DOCX --------------------
@app.post("/export/docx")
def export_docx(req: EquationRequest):
    cleaned = clean_input(req.expression)
    parsed_expr = parse_expression(cleaned)
    solution = solve_expression(parsed_expr)
    steps = generate_steps(parsed_expr, solution)

    filename = "solution.docx"
    filepath = os.path.join("static", filename)

    generate_docx(filepath, req.expression, str(solution), steps)

    return FileResponse(
        filepath,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename
    )

# -------------------- EXPORT BRAILLE --------------------
@app.post("/export/braille")
def export_braille(req: EquationRequest):
    cleaned = clean_input(req.expression)
    parsed_expr = parse_expression(cleaned)
    solution = solve_expression(parsed_expr)

    braille_text = to_braille(str(solution))

    filename = "solution_braille.txt"
    filepath = os.path.join("static", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Ink2Math Braille Output\n\n")
        f.write(braille_text)

    return FileResponse(
        filepath,
        media_type="text/plain",
        filename=filename
    )
