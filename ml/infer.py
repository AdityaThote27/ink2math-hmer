import torch
import csv
import editdistance

from model.hmer_model import HMERModel
from dataset.crohme_dataset import CROHMEDataset

# --------------------------------------------------
# Device
# --------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# --------------------------------------------------
# Load checkpoint
# --------------------------------------------------
checkpoint_path = "checkpoints/ink2math_cnn_lstm_v1.pt"
checkpoint = torch.load(checkpoint_path, map_location=device)

stoi = checkpoint["vocab"]
itos = {v: k for k, v in stoi.items()}
vocab_size = len(stoi)

print("Vocab size:", vocab_size)

# --------------------------------------------------
# Load model
# --------------------------------------------------
model = HMERModel(vocab_size=vocab_size)
model.load_state_dict(checkpoint["model_state"])
model.to(device)
model.eval()

print("✅ Baseline model loaded successfully")

# --------------------------------------------------
# CER (Character Error Rate)
# --------------------------------------------------
def cer(pred, gt):
    """
    Token-level Character Error Rate (CER) for HMER.
    - Computes edit distance on token sequences
    - Normalized by number of GT tokens
    - Clipped to [0, 1] to avoid explosion on short expressions
    """

    pred_tokens = pred.strip().split()
    gt_tokens = gt.strip().split()

    # Empty ground truth (safety check)
    if len(gt_tokens) == 0:
        return 1.0

    import editdistance

    raw_cer = editdistance.eval(pred_tokens, gt_tokens) / len(gt_tokens)

    # Clip CER to [0, 1] for stability and interpretability
    return min(raw_cer, 1.0)



# --------------------------------------------------
# Greedy decoding
# --------------------------------------------------
def greedy_decode(model, image, max_len=100):
    model.eval()

    # start token = 0 (padding)
    tokens = torch.zeros((1, 1), dtype=torch.long).to(device)

    with torch.no_grad():
        enc_out = model.encoder(image)
        context = enc_out.mean(dim=1)

        h = model.init_h(context).unsqueeze(0)
        c = model.init_c(context).unsqueeze(0)

        decoded = []

        for _ in range(max_len):
            logits = model.decoder(enc_out, tokens, (h, c))
            next_token = logits[:, -1].argmax(dim=-1)

            token_id = next_token.item()
            if token_id == 0:
                break

            decoded.append(itos[token_id])
            tokens = torch.cat([tokens, next_token.unsqueeze(1)], dim=1)

    return " ".join(decoded)

# --------------------------------------------------
# Load dataset (for image access)
# --------------------------------------------------
dataset = CROHMEDataset(year="2014")

# Build quick lookup: image_name -> index
img_to_idx = {img: i for i, (img, _) in enumerate(dataset.samples)}

# --------------------------------------------------
# Run inference on test set
# --------------------------------------------------
results = []

with open("test_samples_labeled.txt", "r", encoding="utf-8") as f:
    for line in f:
        img_name, gt, category = line.strip().split("\t")

        idx = img_to_idx[img_name]
        image, _ = dataset[idx]
        image = image.unsqueeze(0).to(device)

        pred = greedy_decode(model, image)
        error = cer(pred, gt)

        results.append([
            img_name,
            category,
            gt,
            pred,
            round(error, 4)
        ])

# --------------------------------------------------
# Save results
# --------------------------------------------------
with open("baseline_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["image", "category", "ground_truth", "prediction", "CER"])
    writer.writerows(results)

print("✅ baseline_results.csv saved")
