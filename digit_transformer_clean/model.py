# model.py
import torch
import torch.nn as nn

class DigitTransformer(nn.Module):
    def __init__(self):
        super().__init__()

        # CNN feature extractor
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=64,
                nhead=4,
                batch_first=True
            ),
            num_layers=2
        )

        self.classifier = nn.Linear(64, 10)

    def forward(self, x):
        x = self.cnn(x)            # (B, 64, H, W)
        B, C, H, W = x.shape

        x = x.view(B, C, H*W).permute(0, 2, 1)
        x = self.transformer(x)
        x = x.mean(dim=1)

        return self.classifier(x)
