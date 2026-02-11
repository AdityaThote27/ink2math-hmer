BRAILLE_MAP = {
    "0": "⠚", "1": "⠁", "2": "⠃", "3": "⠉",
    "4": "⠙", "5": "⠑", "6": "⠋",
    "7": "⠛", "8": "⠓", "9": "⠊",
    "x": "⠭", "+": "⠖", "-": "⠤",
    "=": "⠶"
}

def to_braille(text):
    result = ""
    for char in text:
        result += BRAILLE_MAP.get(char, char)
    return result
