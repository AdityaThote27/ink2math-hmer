# train.py
import torch
import torch.nn as nn
from dataset import get_loader
from model import DigitTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"

loader = get_loader()
model = DigitTransformer().to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

for epoch in range(5):
    total_loss = 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        logits = model(images)
        loss = criterion(logits, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1} - Loss: {total_loss/len(loader):.4f}")

torch.save(model.state_dict(), "digit_transformer.pth")
