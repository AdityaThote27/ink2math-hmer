import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence

from ml.dataset.crohme_dataset import CROHMEDataset
from ml.tokenizer import Tokenizer
from ml.model.hmer_model import HMERModel

# --------------------------------------------------
# Device
# --------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# --------------------------------------------------
# Dataset
# --------------------------------------------------
dataset = CROHMEDataset(year="2014")
labels = [label for _, label in dataset.samples]

# --------------------------------------------------
# Tokenizer
# --------------------------------------------------
tokenizer = Tokenizer()
tokenizer.build_vocab(labels)

print("Vocab size:", tokenizer.vocab_size())

# --------------------------------------------------
# Collate function (padding)
# --------------------------------------------------
def collate_fn(batch):
    images, texts = zip(*batch)
    images = torch.stack(images)

    token_ids = [torch.tensor(tokenizer.encode(t)) for t in texts]
    tokens = pad_sequence(token_ids, batch_first=True, padding_value=0)

    return images, tokens

# --------------------------------------------------
# DataLoader
# --------------------------------------------------
loader = DataLoader(
    dataset,
    batch_size=4,
    shuffle=True,
    collate_fn=collate_fn
)

# --------------------------------------------------
# Model
# --------------------------------------------------
model = HMERModel(vocab_size=tokenizer.vocab_size()).to(device)

criterion = nn.CrossEntropyLoss(ignore_index=0)
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# --------------------------------------------------
# Training Loop
# --------------------------------------------------
EPOCHS = 20   # you can change this (overnight training)

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0.0

    for images, tokens in loader:
        images = images.to(device)
        tokens = tokens.to(device)

        optimizer.zero_grad()

        # Forward
        outputs = model(images, tokens[:, :-1])

        # Loss
        loss = criterion(
            outputs.reshape(-1, outputs.size(-1)),
            tokens[:, 1:].reshape(-1)
        )

        # Backward
        loss.backward()

        # (Optional debug – keep commented after first check)
        # print("Encoder grad:", model.encoder.cnn[0].weight.grad is not None)

        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch + 1} | Loss: {total_loss:.3f}")

# --------------------------------------------------
# Save Model + Vocabulary
# --------------------------------------------------
os.makedirs("ml/checkpoints", exist_ok=True)

torch.save(
    {
        "model_state": model.state_dict(),
        "vocab": tokenizer.stoi
    },
    "ml/checkpoints/hmer_attn_2014.pt"
)

print("✅ Model saved to ml/checkpoints/hmer_attn_2014.pt")
