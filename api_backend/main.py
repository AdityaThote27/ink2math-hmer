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
from recognition.image_ocr import recognize_math_expression

from exports.pdf_export import generate_pdf
from exports.docx_export import generate_docx
from exports.braille_export import to_braille
from exports.voice_export import generate_voice_output, generate_steps_voice_output

from sympy import Poly, symbols, latex
from sympy.parsing.sympy_parser import parse_expr

import os
import shutil
import re

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


# ================= OCR CLEANING =================
def clean_recognized_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\n", " ")
    text = text.replace(".", "")
    text = text.strip()

    # Common OCR math corrections
    replacements = {
        "t": "+",
        "T": "+",
        "l": "1",
        "O": "0",
        "o": "0",
        "—": "-",
        "–": "-",
        "×": "*",
        "÷": "/"
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    # Convert "5 x" → "5*x"
    text = re.sub(r'(\d)\s+([a-zA-Z])', r'\1*\2', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Replace ^ with **
    text = text.replace("^", "**")

    return text.strip()


# ================= EQUATION RECOVERY =================
def recover_equation_if_missing(text: str) -> str:
    if "=" not in text:
        numbers = re.findall(r'\d+', text)
        variables = re.findall(r'[a-zA-Z]', text)

        if variables and len(numbers) >= 2:
            last_number = numbers[-1]
            index = text.rfind(last_number)
            lhs = text[:index]
            rhs = text[index:]
            text = lhs + "=" + rhs

    return text


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
        steps = generate_steps(parsed_expr, solution)

        return {
            "mode": "text",
            "input": req.expression,
            "solution": str(solution),
            "display_latex": display_latex,
            "solution_latex": latex(solution),
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

        parsed_expr = parse_expression(cleaned)
        solution = solve_expression(parsed_expr)
        steps = generate_steps(parsed_expr, solution)

        os.remove(temp_audio_path)

        return {
            "mode": "voice",
            "transcript": transcript,
            "solution": str(solution),
            "display_latex": latex(parsed_expr),
            "solution_latex": latex(solution),
            "steps": steps
        }

    except Exception as e:
        return {"error": str(e)}


# ================= IMAGE SOLVE =================
@app.post("/solve/image")
async def solve_image(file: UploadFile = File(...)):
    try:
        temp_image_path = f"static/temp_{file.filename}"

        with open(temp_image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        recognized_text = recognize_math_expression(temp_image_path)

        if not recognized_text:
            os.remove(temp_image_path)
            return {"error": "Could not recognize expression"}

        cleaned_text = clean_recognized_text(recognized_text)
        cleaned_text = recover_equation_if_missing(cleaned_text)

        # -------- Parse --------
        try:
            if "=" in cleaned_text:
                left_str, right_str = cleaned_text.split("=")
                left_expr = parse_expr(left_str.strip())
                right_expr = parse_expr(right_str.strip())
                parsed_expr = left_expr - right_expr
                display_latex = f"{latex(left_expr)} = {latex(right_expr)}"
            else:
                parsed_expr = parse_expr(cleaned_text)
                display_latex = latex(parsed_expr)

        except Exception as e:
            os.remove(temp_image_path)
            return {
                "recognized_text_raw": recognized_text,
                "recognized_text_cleaned": cleaned_text,
                "error": f"Parsing Error: {str(e)}"
            }

        # -------- Solve Using Core Solver --------
        try:
            solution = solve_expression(parsed_expr)
            steps = generate_steps(parsed_expr, solution)
        except Exception as e:
            os.remove(temp_image_path)
            return {"error": f"Solving Error: {str(e)}"}

        os.remove(temp_image_path)

        return {
            "mode": "image",
            "recognized_text_raw": recognized_text,
            "recognized_text_cleaned": cleaned_text,
            "solution": str(solution),
            "display_latex": display_latex,
            "solution_latex": latex(solution),
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

# ================= DRAW SOLVE =================
@app.post("/solve/draw")
async def solve_draw(file: UploadFile = File(...)):
    try:
        temp_image_path = "static/temp_draw.png"

        with open(temp_image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        recognized_text = recognize_math_expression(temp_image_path)

        if not recognized_text:
            os.remove(temp_image_path)
            return {"error": "Could not recognize drawing"}

        cleaned_text = clean_recognized_text(recognized_text)
        cleaned_text = recover_equation_if_missing(cleaned_text)

        # 🔥 PARSING WITH SAFE ERROR HANDLING
        try:
            if "=" in cleaned_text:
                left_str, right_str = cleaned_text.split("=")
                left_expr = parse_expr(left_str.strip())
                right_expr = parse_expr(right_str.strip())
                parsed_expr = left_expr - right_expr
                display_latex = f"{latex(left_expr)} = {latex(right_expr)}"
            else:
                parsed_expr = parse_expr(cleaned_text)
                display_latex = latex(parsed_expr)
        except Exception as parse_error:
            os.remove(temp_image_path)
            return {
                "error": str(parse_error),
                "recognized_text_raw": recognized_text,
                "recognized_text_cleaned": cleaned_text
            }

        # 🔥 SOLVE
        try:
            solution = solve_expression(parsed_expr)
            steps = generate_steps(parsed_expr, solution)
        except Exception as solve_error:
            os.remove(temp_image_path)
            return {
                "error": str(solve_error),
                "recognized_text_raw": recognized_text,
                "recognized_text_cleaned": cleaned_text
            }

        os.remove(temp_image_path)

        return {
            "mode": "draw",
            "recognized_text_raw": recognized_text,
            "recognized_text_cleaned": cleaned_text,
            "solution": str(solution),
            "display_latex": display_latex,
            "solution_latex": latex(solution),
            "steps": steps
        }

    except Exception as e:
        return {"error": str(e)}
