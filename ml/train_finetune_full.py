import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from ml.models.cnn_transformer.hmer_transformer import HMERTransformer
from ml.dataset.crohme_dataset import CROHMEDataset
from ml.models.cnn_transformer.decoding import ctc_beam_search_decode


# --------------------------------------------------
# Device
# --------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)


# --------------------------------------------------
# Config (VERY IMPORTANT)
# --------------------------------------------------
IMG_HEIGHT = 256
IMG_WIDTH = 256
NUM_CLASSES = 75
BATCH_SIZE = 4          # small batch = stable
EPOCHS = 2              # VERY SMALL
LR = 5e-5               # VERY LOW

LOAD_PATH = "ml/models/cnn_transformer/transformer_with_digit_init.pth"
SAVE_PATH = "ml/models/cnn_transformer/transformer_finetuned.pth"
TOKENIZER_PATH = "ml/models/cnn_transformer/tokenizer_stoi.pth"


# --------------------------------------------------
# Tokenizer
# --------------------------------------------------
stoi = torch.load(TOKENIZER_PATH)
idx_to_token = {v: k for k, v in stoi.items()}


# --------------------------------------------------
# Dataset
# --------------------------------------------------
dataset = CROHMEDataset(year="2014")

loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    drop_last=True
)


# --------------------------------------------------
# Model
# --------------------------------------------------
model = HMERTransformer(
    num_classes=NUM_CLASSES,
    img_height=IMG_HEIGHT,
    img_width=IMG_WIDTH
).to(device)

state = torch.load(LOAD_PATH, map_location=device)
model.load_state_dict(state)

print("✅ Loaded digit-initialized model")


# --------------------------------------------------
# OPTIONAL SAFETY: Freeze encoder (RECOMMENDED)
# --------------------------------------------------
for name, param in model.named_parameters():
    if name.startswith("classifier") or "transformer.layers.3" in name:
        param.requires_grad = True
    else:
        param.requires_grad = False

print("🔓 Training classifier + last transformer layer")



criterion = nn.CTCLoss(blank=0, zero_infinity=True)
optimizer = torch.optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=LR
)


# --------------------------------------------------
# Training Loop
# --------------------------------------------------
model.train()

for epoch in range(EPOCHS):
    total_loss = 0.0

    for images, labels in loader:
        images = images.to(device)

        targets = []
        target_lengths = []

        for lbl in labels:
            encoded = [stoi[ch] for ch in lbl.replace(" ", "") if ch in stoi]
            targets.extend(encoded)
            target_lengths.append(len(encoded))

        targets = torch.tensor(targets, dtype=torch.long).to(device)
        target_lengths = torch.tensor(target_lengths, dtype=torch.long).to(device)

        logits, input_lengths = model(images, return_log_probs=True)

        loss = criterion(
            logits,
            targets,
            input_lengths,
            target_lengths
        )

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(loader)
    print(f"Epoch [{epoch+1}/{EPOCHS}] - Loss: {avg_loss:.4f}")


# --------------------------------------------------
# Save
# --------------------------------------------------
torch.save(model.state_dict(), SAVE_PATH)
print(f"✅ Fine-tuned model saved to: {SAVE_PATH}")
