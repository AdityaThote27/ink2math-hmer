import torch

from ml.models.cnn_transformer.hmer_transformer import HMERTransformer
from ml.models.cnn_transformer.decoding import ctc_beam_search_decode
from ml.dataset.crohme_dataset import CROHMEDataset
from ml.solver.expression_normalizer import normalize_expression
from ml.solver.step_solver import solve_with_steps
from ml.solver.digit_postprocessor import merge_adjacent_digits




# --------------------------------------------------
# Device
# --------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)


# --------------------------------------------------
# Config (MUST match training)
# --------------------------------------------------
IMG_HEIGHT = 256
IMG_WIDTH = 256
NUM_CLASSES = 75
BLANK_IDX = 0

CHECKPOINT_PATH = "ml/models/cnn_transformer/transformer_finetuned.pth"
TOKENIZER_PATH = "ml/models/cnn_transformer/tokenizer_stoi.pth"


# --------------------------------------------------
# Load tokenizer vocab
# --------------------------------------------------
stoi = torch.load(TOKENIZER_PATH)
idx_to_token = {v: k for k, v in stoi.items()}

print("Tokenizer size:", len(stoi))
print("Max token id in tokenizer:", max(stoi.values()))
assert BLANK_IDX in idx_to_token, "Blank token index missing"


# --------------------------------------------------
# Load model
# --------------------------------------------------
model = HMERTransformer(
    num_classes=NUM_CLASSES,
    img_height=IMG_HEIGHT,
    img_width=IMG_WIDTH
).to(device)

checkpoint = torch.load(CHECKPOINT_PATH, map_location=device)
model.load_state_dict(checkpoint)

model.eval()
print("✅ Transformer model loaded")


# --------------------------------------------------
# Load dataset
# --------------------------------------------------
dataset = CROHMEDataset(year="2014")


# --------------------------------------------------
# Inference (SAFE, FIXED, FINAL)
# --------------------------------------------------
for i in range(20):
    image, gt = dataset[i]

    # FORCE image to (B, C, H, W)
    if image.dim() == 2:
        image = image.unsqueeze(0).unsqueeze(0)   # (1,1,H,W)
    elif image.dim() == 3:
        image = image.unsqueeze(0)                # (1,1,H,W)
    elif image.dim() == 4:
        pass                                      # already correct
    else:
        raise ValueError(f"Unexpected image shape: {image.shape}")

    image = image.to(device)

    with torch.no_grad():
        logits, _ = model(image, return_log_probs=False)
        logits = torch.log_softmax(logits, dim=-1)

        decoded = ctc_beam_search_decode(
            logits=logits,
            idx_to_token=idx_to_token,
            beam_width=5,
            blank_idx=BLANK_IDX,
            
        )

raw_pred = decoded[0]

# Step 1: normalize OCR output
normalized = normalize_expression(raw_pred)

# Step 2: merge adjacent digits (post-processing)
postprocessed = merge_adjacent_digits(normalized) if normalized else None


print(f"\nGT: {gt}")
print(f"Raw OCR: {raw_pred}")
print(f"Normalized: {normalized}")
print(f"Postprocessed: {postprocessed}")

if postprocessed:
    result, steps = solve_with_steps(postprocessed)
    print("Steps:")
    for s in steps:
        print("  ", s)
    print("Result:", result)
else:
    print("Expression rejected (invalid)")



