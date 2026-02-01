import pandas as pd

from ml.utils.math_normalizer import normalize_expression, repair_expression
from ml.utils.math_solver import solve_expression


CSV_PATH = "transformer_results3.csv"   # the file that took 2 hours


print("=== Testing Repair + Solver on Existing Results ===\n")

df = pd.read_csv(CSV_PATH)

found = 0

for i, row in df.iterrows():
    raw = str(row["raw_prediction"])

    normalized = normalize_expression(raw)
    repaired = repair_expression(normalized)
    solution = solve_expression(repaired)

    if solution is not None:
        print("RAW        :", raw)
        print("NORMALIZED :", normalized)
        print("REPAIRED   :", repaired)
        print("SOLUTION   :", solution)
        print("-" * 50)

        found += 1

    if found >= 5:   # stop after a few successes
        break

if found == 0:
    print("❌ No solvable expressions found yet.")
else:
    print(f"✅ Found {found} solvable expressions.")
