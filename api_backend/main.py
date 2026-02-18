from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from models.schemas import EquationRequest

from core.parser import parse_expression
from core.solver import solve_expression
from core.steps_generator import generate_steps
from core.utils import clean_input
from core.voice_normalizer import normalize_speech

from recognition.voice_asr import VoiceASR

from exports.pdf_export import generate_pdf
from exports.docx_export import generate_docx
from exports.braille_export import to_braille
from exports.voice_export import generate_voice_output, generate_steps_voice_output

from sympy import Poly, symbols, latex

import os
import shutil

app = FastAPI()

voice_model = VoiceASR()

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists("static"):
    os.makedirs("static")


# -------------------- HOME --------------------
@app.get("/")
def home():
    return {"message": "Ink2Math Backend Running"}


# ================= TEXT SOLVE =================
@app.post("/solve")
def solve_equation(req: EquationRequest):
    try:
        cleaned = clean_input(req.expression)

        if "=" in cleaned:
            left_str, right_str = cleaned.split("=")
            left_expr = parse_expression(left_str.strip())
            right_expr = parse_expression(right_str.strip())

            parsed_expr = left_expr - right_expr
            display_latex = f"{latex(left_expr)} = {latex(right_expr)}"
        else:
            parsed_expr = parse_expression(cleaned)
            display_latex = latex(parsed_expr)

        solution = solve_expression(parsed_expr)

        if isinstance(solution, list):
            clean_solution = ", ".join([str(s) for s in solution])
            solution_latex = ", ".join([latex(s) for s in solution])
        else:
            clean_solution = str(solution)
            solution_latex = latex(solution)

        x = symbols("x")
        try:
            poly = Poly(parsed_expr, x)
            degree = poly.degree()
        except:
            degree = None

        if degree == 1:
            equation_type = "Linear Equation"
        elif degree == 2:
            equation_type = "Quadratic Equation"
        elif parsed_expr.free_symbols:
            equation_type = "General Expression"
        else:
            equation_type = "Arithmetic Expression"

        steps = generate_steps(parsed_expr, solution)

        return {
            "mode": "text",
            "input": req.expression,
            "type": equation_type,
            "solution": clean_solution,
            "display_latex": display_latex,
            "solution_latex": solution_latex,
            "steps": steps
        }

    except Exception as e:
        return {"error": str(e)}


# ================= VOICE SOLVE =================
@app.post("/solve/voice")
async def solve_voice(file: UploadFile = File(...)):
    try:
        temp_audio_path = f"static/temp_{file.filename}"

        with open(temp_audio_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcript = voice_model.transcribe(temp_audio_path)
        normalized = normalize_speech(transcript)
        cleaned = clean_input(normalized)

        if "=" in cleaned:
            left_str, right_str = cleaned.split("=")
            left_expr = parse_expression(left_str.strip())
            right_expr = parse_expression(right_str.strip())

            parsed_expr = left_expr - right_expr
            display_latex = f"{latex(left_expr)} = {latex(right_expr)}"
        else:
            parsed_expr = parse_expression(cleaned)
            display_latex = latex(parsed_expr)

        solution = solve_expression(parsed_expr)

        if isinstance(solution, list):
            clean_solution = ", ".join([str(s) for s in solution])
            solution_latex = ", ".join([latex(s) for s in solution])
        else:
            clean_solution = str(solution)
            solution_latex = latex(solution)

        x = symbols("x")
        try:
            poly = Poly(parsed_expr, x)
            degree = poly.degree()
        except:
            degree = None

        if degree == 1:
            equation_type = "Linear Equation"
        elif degree == 2:
            equation_type = "Quadratic Equation"
        elif parsed_expr.free_symbols:
            equation_type = "General Expression"
        else:
            equation_type = "Arithmetic Expression"

        steps = generate_steps(parsed_expr, solution)

        os.remove(temp_audio_path)

        return {
            "mode": "voice",
            "transcript": transcript,
            "normalized_expression": normalized,
            "type": equation_type,
            "solution": clean_solution,
            "display_latex": display_latex,
            "solution_latex": solution_latex,
            "steps": steps
        }

    except Exception as e:
        return {"error": str(e)}


# ================= EXPORT PDF =================
@app.post("/export/pdf")
def export_pdf(req: EquationRequest):
    cleaned = clean_input(req.expression)
    parsed_expr = parse_expression(cleaned)
    solution = solve_expression(parsed_expr)
    steps = generate_steps(parsed_expr, solution)

    filename = "solution.pdf"
    filepath = os.path.join("static", filename)

    generate_pdf(filepath, req.expression, str(solution), steps)

    return FileResponse(filepath, media_type="application/pdf", filename=filename)


# ================= EXPORT DOCX =================
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


# ================= EXPORT BRAILLE =================
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

    return FileResponse(filepath, media_type="text/plain", filename=filename)


# ================= EXPORT VOICE =================
@app.post("/export/voice")
def export_voice(req: EquationRequest):
    cleaned = clean_input(req.expression)
    parsed_expr = parse_expression(cleaned)
    solution = solve_expression(parsed_expr)

    solution_text = str(solution)
    speech_text = f"The solution is {solution_text}. Please check the steps for explanation."

    filepath = generate_voice_output(speech_text)

    return FileResponse(
        filepath,
        media_type="audio/mpeg",
        filename="solution_voice.mp3"
    )


# ================= EXPORT VOICE WITH STEPS =================
@app.post("/export/voice/steps")
def export_voice_steps(req: EquationRequest):
    cleaned = clean_input(req.expression)
    parsed_expr = parse_expression(cleaned)
    solution = solve_expression(parsed_expr)
    steps = generate_steps(parsed_expr, solution)

    solution_text = str(solution)

    filepath = generate_steps_voice_output(
        req.expression,
        steps,
        solution_text
    )

    return FileResponse(
        filepath,
        media_type="audio/mpeg",
        filename="solution_steps_voice.mp3"
    )
