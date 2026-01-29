import torch
import torch.nn as nn
import math


class FeedForward(nn.Module):
    def __init__(self, embed_dim, hidden_dim, dropout=0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(embed_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, embed_dim)
        )

    def forward(self, x):
        # x: (batch, seq_len, embed_dim)
        return self.net(x)


class MultiHeadSelfAttention(nn.Module):
    def __init__(self, embed_dim, num_heads, dropout=0.1):
        super().__init__()
        assert embed_dim % num_heads == 0, "embed_dim must be divisible by num_heads"

        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        self.qkv_proj = nn.Linear(embed_dim, embed_dim * 3)
        self.out_proj = nn.Linear(embed_dim, embed_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # x: (batch, seq_len, embed_dim)
        B, T, E = x.shape

        qkv = self.qkv_proj(x)                       # (B, T, 3E)
        qkv = qkv.reshape(B, T, 3, self.num_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)              # (3, B, heads, T, head_dim)

        q, k, v = qkv[0], qkv[1], qkv[2]

        attn_scores = torch.matmul(q, k.transpose(-2, -1))
        attn_scores = attn_scores / math.sqrt(self.head_dim)

        attn_weights = torch.softmax(attn_scores, dim=-1)
        attn_weights = self.dropout(attn_weights)

        attn_output = torch.matmul(attn_weights, v)  # (B, heads, T, head_dim)
        attn_output = attn_output.transpose(1, 2).reshape(B, T, E)

        return self.out_proj(attn_output)


class TransformerEncoderBlock(nn.Module):
    def __init__(self, embed_dim, num_heads, ff_hidden_dim, dropout=0.1):
        super().__init__()

        self.self_attn = MultiHeadSelfAttention(embed_dim, num_heads, dropout)
        self.ffn = FeedForward(embed_dim, ff_hidden_dim, dropout)

        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # Self-attention block
        attn_out = self.self_attn(x)
        x = self.norm1(x + self.dropout(attn_out))

        # Feed-forward block
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))

        return x


class TransformerEncoder(nn.Module):
    def __init__(
        self,
        embed_dim=256,
        num_heads=8,
        num_layers=4,
        ff_hidden_dim=1024,
        dropout=0.1
    ):
        super().__init__()

        self.layers = nn.ModuleList([
            TransformerEncoderBlock(
                embed_dim=embed_dim,
                num_heads=num_heads,
                ff_hidden_dim=ff_hidden_dim,
                dropout=dropout
            )
            for _ in range(num_layers)
        ])

    def forward(self, x):
        # x: (batch, seq_len, embed_dim)
        for layer in self.layers:
            x = layer(x)
        return x
