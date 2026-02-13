import re

WORD_TO_SYMBOL = {
    "plus": "+",
    "minus": "-",
    "equals": "=",
    "multiplied by": "*",
    "divided by": "/",
    "squared": "^2",
    "cubed": "^3"
}

NUMBER_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10"
}

def normalize_speech(text: str) -> str:
    text = text.lower()

    # Replace number words
    for word, digit in NUMBER_WORDS.items():
        text = re.sub(rf"\b{word}\b", digit, text)

    # Replace math phrases (longest first)
    for phrase in sorted(WORD_TO_SYMBOL, key=len, reverse=True):
        text = text.replace(phrase, WORD_TO_SYMBOL[phrase])

    return text
