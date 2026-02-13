import pyttsx3
import os
import time

def _configure_engine():
    engine = pyttsx3.init()

    # Slower and clearer speech
    engine.setProperty('rate', 145)
    engine.setProperty('volume', 1.0)

    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)

    return engine


def generate_voice_output(text: str, filename: str = "solution_voice.mp3") -> str:
    engine = _configure_engine()

    if not os.path.exists("static"):
        os.makedirs("static")

    filepath = os.path.join("static", filename)

    engine.save_to_file(text, filepath)
    engine.runAndWait()

    return filepath


def generate_steps_voice_output(equation_text: str, steps: list, solution_text: str,
                                filename: str = "solution_steps_voice.mp3") -> str:
    """
    Generates a narrated step-by-step explanation.
    """

    engine = _configure_engine()

    if not os.path.exists("static"):
        os.makedirs("static")

    filepath = os.path.join("static", filename)

    # Build narration text
    narration = f"The equation is {equation_text}. "

    for step in steps:
        narration += f"Step {step['step']}. {step['title']}. {step['description']}. "

    narration += f"Final answer. The solution is {solution_text}."

    engine.save_to_file(narration, filepath)
    engine.runAndWait()

    return filepath
