import torch
import torch.nn as nn

from .cnn_backbone import CNNBackbone
from .positional_encoding import PositionalEncoding2D
from .transformer_encoder import TransformerEncoder


class HMERTransformer(nn.Module):
    """
    End-to-end Handwritten Math Expression Recognition model
    using CNN + Transformer Encoder + CTC-compatible output.
    """

    def __init__(
        self,
        num_classes,
        img_height=128,
        img_width=512,
        embed_dim=256,
        num_heads=8,
        num_layers=4,
        ff_hidden_dim=1024,
        dropout=0.1
    ):
        super().__init__()

        # 1️⃣ CNN Backbone
        self.cnn = CNNBackbone(in_channels=1, out_channels=embed_dim)

        # CNN downsamples by factor of 8 (3 MaxPools)
        self.feature_h = img_height // 8
        self.feature_w = img_width // 8
        self.seq_len = self.feature_h * self.feature_w

        # 2️⃣ 2D Positional Encoding
        self.positional_encoding = PositionalEncoding2D(
            embed_dim=embed_dim,
            height=self.feature_h,
            width=self.feature_w
        )

        # 3️⃣ Transformer Encoder
        self.transformer = TransformerEncoder(
            embed_dim=embed_dim,
            num_heads=num_heads,
            num_layers=num_layers,
            ff_hidden_dim=ff_hidden_dim,
            dropout=dropout
        )

        # 4️⃣ Output projection (CTC-ready)
        self.classifier = nn.Linear(embed_dim, num_classes)

    def forward(self, x, return_log_probs=False):
        """
        Args:
            x: (batch, 1, H, W)
            return_log_probs: bool (for CTC loss / decoding)

        Returns:
            logits or log_probs: (seq_len, batch, num_classes)
            seq_len: int (needed for CTC inference)
        """

        # 🔹 CNN feature extraction
        features = self.cnn(x)
        # (B, C, H', W')

        B, C, H, W = features.shape

        # 🔹 Flatten spatial grid → token sequence
        features = features.permute(0, 2, 3, 1)       # (B, H', W', C)
        features = features.contiguous().view(B, H * W, C)
        # (B, seq_len, embed_dim)

        # 🔹 Add 2D positional encoding
        features = self.positional_encoding(features)

        # 🔹 Transformer encoding
        encoded = self.transformer(features)
        # (B, seq_len, embed_dim)

        # 🔹 Project to symbol logits
        logits = self.classifier(encoded)
        # (B, seq_len, num_classes)

        # 🔹 CTC expects (seq_len, batch, num_classes)
        logits = logits.permute(1, 0, 2)

        if return_log_probs:
            logits = torch.log_softmax(logits, dim=2)

        return logits, logits.size(0)
