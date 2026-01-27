import torch.nn as nn
from torchvision import models

class CNNEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        base = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        base.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.cnn = nn.Sequential(*list(base.children())[:-2])

    def forward(self, x):
        f = self.cnn(x)            # [B, C, H, W]
        b, c, h, w = f.size()
        f = f.permute(0, 2, 3, 1)  # [B, H, W, C]
        return f.view(b, h*w, c)   # [B, T, C]
