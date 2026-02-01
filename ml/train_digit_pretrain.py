import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from ml.models.cnn_transformer.hmer_transformer import HMERTransformer
from ml.dataset.augmented_digit_dataset import AugmentedDigitDataset
from ml.tokenizer.digit_tokenizer import DigitCTCTokenizer


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
NUM_CLASSES = 11          # blank + digits 0–9
BATCH_SIZE = 8
EPOCHS = 6                # keep small
LR = 1e-4

SAVE_PATH = "ml/models/cnn_transformer/transformer_digit_pretrained.pth"


# --------------------------------------------------
# Dataset & Tokenizer
# --------------------------------------------------
tokenizer = DigitCTCTokenizer()
dataset = AugmentedDigitDataset(year="2014", repeat_factor=50)

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

criterion = nn.CTCLoss(blank=0, zero_infinity=True)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)


# --------------------------------------------------
# Training Loop
# --------------------------------------------------
model.train()

for epoch in range(EPOCHS):
    total_loss = 0.0

    for images, labels in loader:
        images = images.to(device)

        # Encode labels
        targets = []
        target_lengths = []

        for lbl in labels:
            encoded = tokenizer.encode(lbl)
            targets.extend(encoded)
            target_lengths.append(len(encoded))

        targets = torch.tensor(targets, dtype=torch.long).to(device)
        target_lengths = torch.tensor(target_lengths, dtype=torch.long).to(device)

        # Forward
        logits, input_lengths = model(images, return_log_probs=True)

        # input_lengths already correct shape
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
# Save checkpoint
# --------------------------------------------------
torch.save(model.state_dict(), SAVE_PATH)
print(f"✅ Digit-pretrained model saved to: {SAVE_PATH}")
