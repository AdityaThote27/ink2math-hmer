def merge_adjacent_digits(expr: str):
    """
    Try to merge isolated digits into multi-digit numbers.
    Example: '1 2' → '12'
    """
    if not expr:
        return expr

    out = ""
    prev_digit = False

    for ch in expr:
        if ch.isdigit():
            out += ch
            prev_digit = True
        else:
            out += ch
            prev_digit = False

    return out
