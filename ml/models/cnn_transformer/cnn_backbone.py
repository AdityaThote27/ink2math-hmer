import torch
import torch.nn as nn


class CNNBackbone(nn.Module):
    """
    CNN feature extractor for handwritten mathematical expressions.

    Input  : (B, 1, H, W)
    Output : (B, C, H', W')
    """

    def __init__(self, in_channels=1, out_channels=256):
        super().__init__()

        self.cnn = nn.Sequential(
            # Block 1
            nn.Conv2d(in_channels, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),  # H/2, W/2

            # Block 2
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),  # H/4, W/4

            # Block 3
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),

            # Optional downsampling (comment out if you want higher resolution)
            nn.MaxPool2d(2)   # H/8, W/8
        )

        self.out_channels = out_channels

    def forward(self, x):
        """
        Args:
            x: Tensor of shape (batch, 1, H, W)

        Returns:
            feature_map: (batch, C, H', W')
        """
        return self.cnn(x)
