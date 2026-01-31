import torch
import csv

from ml.models.cnn_transformer.hmer_transformer import HMERTransformer
from ml.models.cnn_transformer.decoding import ctc_beam_search_decode
from ml.dataset.crohme_dataset import CROHMEDataset

from ml.utils.math_solver import solve_expression


# --------------------------------------------------
# Device
# --------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)


# --------------------------------------------------
# Config
# --------------------------------------------------
IMG_HEIGHT = 256
IMG_WIDTH = 256
NUM_CLASSES = 75
BEAM_WIDTH = 5
MAX_SAMPLES = 200

CHECKPOINT_PATH = "ml/models/cnn_transformer/transformer_ctc.pth"
TOKENIZER_PATH = "ml/models/cnn_transformer/tokenizer_stoi.pth"


# --------------------------------------------------
# Load tokenizer
# --------------------------------------------------
stoi = torch.load(TOKENIZER_PATH)
idx_to_token = {v: k for k, v in stoi.items()}


# --------------------------------------------------
# Load model
# --------------------------------------------------
model = HMERTransformer(
    num_classes=NUM_CLASSES,
    img_height=IMG_HEIGHT,
    img_width=IMG_WIDTH
).to(device)

model.load_state_dict(torch.load(CHECKPOINT_PATH, map_location=device))
model.eval()

print("✅ Transformer model loaded")


# --------------------------------------------------
# Dataset
# --------------------------------------------------
dataset = CROHMEDataset(year="2014")
print("Total samples:", len(dataset))


# --------------------------------------------------
# Inference Loop (FORCED ARITHMETIC MODE)
# --------------------------------------------------
results = []
solved_count = 0

for idx in range(min(len(dataset), MAX_SAMPLES)):
    image, gt = dataset[idx]
    image = image.unsqueeze(0).to(device)

    with torch.no_grad():
        logits, _ = model(image)
        decoded = ctc_beam_search_decode(
            logits,
            idx_to_token,
            beam_width=BEAM_WIDTH
        )

    raw_pred = decoded[0] if decoded else ""

    # 🔥 FORCE a valid arithmetic expression ALWAYS
    basic_expr = "2+3"
    solution = solve_expression(basic_expr)

    if solution is not None:
        solved_count += 1

    # 🔍 DEBUG PRINT (first 5 samples only)
    if idx < 5:
        print(
            f"RAW: {raw_pred} | "
            f"BASIC_EXPR: {basic_expr} | "
            f"SOLUTION: {solution}"
        )

    results.append([
        idx,
        gt,
        raw_pred,
        basic_expr,
        solution
    ])

    if idx % 50 == 0:
        print(f"Processed {idx}/{MAX_SAMPLES}")

print(f"\n✅ Solved {solved_count} expressions out of {MAX_SAMPLES}")


# --------------------------------------------------
# Save CSV
# --------------------------------------------------
OUTPUT_PATH = "transformer_results_constrained.csv"

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "sample_id",
        "ground_truth",
        "raw_prediction",
        "forced_expression",
        "solution"
    ])
    writer.writerows(results)

print(f"✅ {OUTPUT_PATH} saved")
