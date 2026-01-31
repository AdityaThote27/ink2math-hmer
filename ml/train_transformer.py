import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from dataset.crohme_dataset import CROHMEDataset
from tokenizer_ctc import CTCTokenizer
from models.cnn_transformer.hmer_transformer import HMERTransformer


# --------------------------------------------------
# Device
# --------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)


# --------------------------------------------------
# Dataset (manual year-wise split)
# --------------------------------------------------
train_dataset = CROHMEDataset(year="2014")

labels = [label for _, label in train_dataset.samples]


# --------------------------------------------------
# CTC Tokenizer
# --------------------------------------------------
tokenizer = CTCTokenizer()
tokenizer.build_vocab(labels)

num_classes = tokenizer.vocab_size()
print("CTC Vocab size:", num_classes)


# --------------------------------------------------
# CTC Collate Function
# --------------------------------------------------
def ctc_collate_fn(batch):
    images, labels = zip(*batch)

    # Stack images
    images = torch.stack(images)  # (B, 1, H, W)

    # Encode labels
    encoded = [
        torch.tensor(tokenizer.encode(lbl), dtype=torch.long)
        for lbl in labels
    ]

    target_lengths = torch.tensor(
        [len(t) for t in encoded],
        dtype=torch.long
    )

    # CTC requires targets as a 1D tensor
    targets = torch.cat(encoded)

    return images, targets, target_lengths


# --------------------------------------------------
# DataLoader
# --------------------------------------------------
train_loader = DataLoader(
    train_dataset,
    batch_size=2,      # small batch for CPU sanity check
    shuffle=True,
    num_workers=0,
    collate_fn=ctc_collate_fn
)


# --------------------------------------------------
# Model
# --------------------------------------------------
model = HMERTransformer(
    num_classes=num_classes,
    img_height=256,   # MUST stay fixed (positional encoding)
    img_width=256,
    embed_dim=256,
    num_heads=8,
    num_layers=4
).to(device)


# --------------------------------------------------
# Loss & Optimizer (CTC)
# --------------------------------------------------
criterion = nn.CTCLoss(blank=0, zero_infinity=True)
optimizer = optim.Adam(model.parameters(), lr=1e-4)


# --------------------------------------------------
# Training Loop (Sanity Check)
# --------------------------------------------------
model.train()

for epoch in range(25):  # 1 epoch = sanity check
    print(f"\nEpoch {epoch + 1}")

    for batch_idx, (images, targets, target_lengths) in enumerate(train_loader):
        images = images.to(device)
        targets = targets.to(device)
        target_lengths = target_lengths.to(device)

        optimizer.zero_grad()

        # Forward pass
        logits, seq_len = model(images)
        # logits: (seq_len, batch, num_classes)

        log_probs = logits.log_softmax(dim=2)

        batch_size = log_probs.size(1)
        input_lengths = torch.full(
            size=(batch_size,),
            fill_value=seq_len,
            dtype=torch.long
        ).to(device)

        # CTC Loss
        loss = criterion(
            log_probs,
            targets,
            input_lengths,
            target_lengths
        )

        loss.backward()
        optimizer.step()

        print(f"Batch {batch_idx} | Loss: {loss.item():.4f}")

        # 🔴 Stop early for sanity
        if batch_idx == 1:
            print("✅ Transformer + CTC sanity check passed")
            break


# --------------------------------------------------
# Save Model & Tokenizer (🔥 CRITICAL)
# --------------------------------------------------
os.makedirs("ml/models/cnn_transformer", exist_ok=True)

# Save model weights
torch.save(
    model.state_dict(),
    "ml/models/cnn_transformer/transformer_ctc.pth"
)

# Save tokenizer vocab (stoi)
torch.save(
    tokenizer.stoi,
    "ml/models/cnn_transformer/tokenizer_stoi.pth"
)

print("✅ Transformer checkpoint saved")
print("✅ Tokenizer vocab saved")
print("🚀 Training script finished")
