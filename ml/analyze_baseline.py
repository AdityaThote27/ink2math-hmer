import csv
from collections import defaultdict

cer_by_cat = defaultdict(list)

with open("baseline_results.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cer_by_cat[row["category"]].append(float(row["CER"]))

print("Average CER by category:")
for cat, values in cer_by_cat.items():
    avg = sum(values) / len(values)
    print(f"{cat}: {avg:.4f}")
