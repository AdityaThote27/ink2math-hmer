def clean_symbol_sequence(symbols):
    """
    Cleans a raw symbol sequence using math syntax rules.

    Rules:
    - Expression cannot start with operator
    - Expression cannot end with operator
    - No consecutive operators
    """

    if not symbols:
        return []

    cleaned = []

    prev_is_op = True  # treat start as operator to block leading ops

    for s in symbols:
        is_op = s in {"+", "-", "*", "/"}

        # Skip leading operator
        if prev_is_op and is_op:
            continue

        cleaned.append(s)
        prev_is_op = is_op

    # Remove trailing operator
    if cleaned and cleaned[-1] in {"+", "-", "*", "/"}:
        cleaned.pop()

    return cleaned
