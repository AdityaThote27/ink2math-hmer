def classify_expression(expr):
    symbols = expr.split()

    if any(op in expr for op in ["\\frac", "\\sqrt", "^", "_", "\\int"]):
        return "complex"

    if len(symbols) <= 5:
        return "simple"
    elif len(symbols) <= 12:
        return "medium"
    else:
        return "complex"


counts = {"simple": 0, "medium": 0, "complex": 0}

with open("test_samples.txt", "r", encoding="utf-8") as f, \
     open("test_samples_labeled.txt", "w", encoding="utf-8") as out:

    for line in f:
        img, label = line.strip().split("\t")
        category = classify_expression(label)
        counts[category] += 1
        out.write(f"{img}\t{label}\t{category}\n")

print("Category distribution:")
for k, v in counts.items():
    print(f"{k}: {v}")
